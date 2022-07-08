from django.urls import reverse
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from core.utils import Util
import jwt
from django.conf import settings
from rest_framework import views
from rest_framework.generics import (
                        ListAPIView,
                        CreateAPIView,
                        RetrieveUpdateDestroyAPIView,
                        )

from user.models import UserAddress

from .serializers import (
    RegisterSerializer,
    EmployeeRegisterSerializer, 
    EmailVerificationSerializer, 
    LoginSerializer,
    LogoutSerializer)
from core.permissions import IsNotAuthenticated, AddressOwnerOnly
from rest_framework.permissions import IsAdminUser

from user import serializers

User =get_user_model()

class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    #permission_classes = (IsNotAuthenticated,)

    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.first_name + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmployeeRegisterAPIView(generics.GenericAPIView):
    serializer_class = EmployeeRegisterSerializer
    permission_classes = (IsAdminUser, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)    
        serializer.save()
        return Response({'message':'Employee Successfull created'}, status=status.HTTP_201_CREATED)   

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserAddressListAPIView(ListAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = serializers.UserAddressSerializer

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

class UserAddressCreateAPIView(CreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = serializers.UserAddressCreateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserAddressRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = serializers.UserAddressSerializer
    permission_classes = (AddressOwnerOnly,)

import datetime
from django.contrib import auth
from requests import request
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password','first_name', 'last_name', 'birth_year']

    def validate(self, attrs):
        email = attrs.get('email', '')
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        birth_year = attrs.get('birth_year', '')
        
        current_year = datetime.datetime.now().year
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already exist')
        if current_year - int(birth_year) < 16 and current_year - int(birth_year) > 0: 
            raise serializers.ValidationError("User's age must over 16")
        elif int(birth_year) >= current_year or current_year-int(birth_year)>100:
            raise serializers.ValidationError('Please enter valid date year!')
        # if first_name.isalnum() or last_name.isalnum():
        #     raise serializers.ValidationError(
        #         'The First Name or Last Name should only text')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            birth_year = validated_data['birth_year'],
            password = validated_data['password'],
        )
        user.is_active = False 
        user.save()
        return user
    
    
   
class EmailVerificationSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj.email)

        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)

        user = auth.authenticate(email=email, password=password)
        # print(user)
        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        # print(user)

        if not user:
            raise AuthenticationFailed('Invalid credentials!')
        if not user.is_active:
            raise AuthenticationFailed('Acc is not active') #BUG 
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')

        return user

        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
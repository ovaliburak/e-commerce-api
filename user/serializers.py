from dataclasses import fields
import datetime
from django.contrib import auth
from django.forms import ValidationError
from requests import request
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from . import models 


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password','first_name', 'last_name', 'birth_year']

    def validate(self, attrs):
        email = attrs.get('email', '')
        birth_year = attrs.get('birth_year', '')  
        current_year = datetime.datetime.now().year
    
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already exist')
        if current_year - int(birth_year) < 16 and current_year - int(birth_year) > 0: 
            raise serializers.ValidationError("User's age must over 16")
        elif int(birth_year) >= current_year or current_year-int(birth_year)>100:
            raise serializers.ValidationError('Please enter valid date year!')
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
    
class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password','first_name', 'last_name', 'birth_year']

    def validate(self, attrs):
        email = attrs.get('email', '')
        birth_year = attrs.get('birth_year', '')
        current_year = datetime.datetime.now().year
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already exist')
        if current_year - int(birth_year) < 16 and current_year - int(birth_year) > 0: 
            raise serializers.ValidationError("User's age must over 16")
        elif int(birth_year) >= current_year or current_year-int(birth_year)>100:
            raise serializers.ValidationError('Please enter valid date year!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_employee(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            birth_year = validated_data['birth_year'],
            password = validated_data['password'],
        )
        user.is_active = True  
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
        return {'refresh': user.tokens['refresh'], 
                'access': user.tokens['access']}
    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials!')
        if not user.is_active:
            raise AuthenticationFailed('Acc is not active') #BUG 
 
        return user

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

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.UserAddress
        fields = '__all__'

class UserAddressCreateSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = models.UserAddress
        exclude = ('user', )

    def validate(self, attrs):
        address_line1 = attrs.get('address_line1', None)
        address_line2 = attrs.get('address_line2', None)
        # city = attrs.get('city', None)
        # postal_code = attrs.get('postal_code', None)
        # country = attrs.get('country', None)
        # phone = attrs.get('phone', None)
        if address_line1 is None:
            raise ValidationError('User must have a address line 1!')
        elif address_line1 == address_line2:
            raise ValidationError('Two address line must be different!')
        return attrs
        
    # def create(self, validated_data):
    #     user = self.request.user
    #     user_address = models.UserAddress(user=user, **validated_data)
    #     user_address.save()
    #     return user_address
        
class UserSerializer(serializers.ModelSerializer):
    user_address = UserAddressSerializer()
    class Meta:
        model = User
        fields = '__all__'
        
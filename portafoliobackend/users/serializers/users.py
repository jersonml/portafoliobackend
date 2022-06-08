#Django
from django.conf import settings
from django.contrib.auth import authenticate,password_validation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.validators import RegexValidator

#Django Rest Framekwork
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Library
from datetime import timedelta
import jwt

#Permissions
from knox.models import AuthToken


#Models
from portafoliobackend.users.models import Users
from portafoliobackend.users.models.profiles import Profile

#Serializer
from portafoliobackend.users.serializers.profile import (
    ListProfileModelSerializer, 
    ProfileModelSerializer
)

class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)
    
    class Meta:

        model = Users
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'country',
            'profile',
        )

class ListUserModelSerializer(serializers.ModelSerializer):
    profile = ListProfileModelSerializer(read_only=True)

    class Meta:

        model = Users
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'country',
            'profile',
        )

class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,max_length = 128)

    def validate(self, attrs):
        user = authenticate(username= attrs['email'],password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User inactive')
        self.context['user'] = user
        return attrs

    def create(self, validated_data):
        token= AuthToken.objects.create(self.context['user'])[1]
        self.context['token'] = token
        return self.context['user']

    def to_representation(self, instance):
        return {
            'user': self.context['user'],
            'access_token': self.context['token']
        }

class AccountVerificationSerializer(serializers.Serializer):
    
    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link as expired")
        except jwt.PyJWTError:
            raise serializers.ValidationError("Invalid Token")
        
        if payload['type'] != "email_confirmation":
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload

        return data

    def save(self):
        payload = self.context['payload']
        user = Users.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()

    def to_representation(self, instance):
        return {
             'message': 'Congratulation,Welcome!'
        }

class UserSignupSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=Users.objects.all()
            )
        ]
    )
    username = serializers.CharField(
        min_length = 4,
        max_length = 20,
        validators=[
            UniqueValidator(
                queryset=Users.objects.all()    
            )
        ]
    )
    phone_regex= RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999 up to 15 digits allowed"
    )

    phone_number= serializers.CharField(
        max_length=17, validators=[phone_regex]
    )

    password = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self,data):
        password = data['password']
       
        password_validation.validate_password(password)
        return data

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data, is_verified=False)
        Profile.objects.create(user= user)
        self.send_confirmation_email(user)
        self.context['token'] = AuthToken.objects.get_or_create(self.context['user'])[1]
        return user
    
    def send_confirmation_email(self,user):
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username} verify your account to start using Portaolio'
        from_email = "Portafolio <xljersonlx@gmail.com>"
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token,'user':user}
        )
        text_content = 'This is an important message.'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
        print('sending email')

    def gen_verification_token(self,user):
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    
    def to_representation(self, instance):
        return {
            'user': self.context['user'],
            'access_token': self.context['token']
        }

#Documentation
class ResponseUserModelSerializer(serializers.Serializer):

    user =  UserModelSerializer(many=True, read_only=True)
    access_token = serializers.CharField()

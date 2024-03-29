#Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
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

#Models
from portafoliobackend.users.models import Users
from portafoliobackend.users.models.profiles import Profile

#Serializer
from portafoliobackend.users.serializers.profile import (
    BaseProfileModelSerializer, 
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
    
    profile = BaseProfileModelSerializer(read_only=True)

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
   
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

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

class UserSignupSerializer(serializers.ModelSerializer):

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

    class Meta:
        model= Users
        fields = [
            'email',
            'username',
            'password',
            'phone_number',
            'first_name',
            'last_name',
            'country',
            'document'
        ]

    def validate(self,data):
        password = data['password']
       
        password_validation.validate_password(password)
        return data

    def create(self, validated_data):
        user = Users.objects.create_user(
            **validated_data, 
            is_verified=False
        )
        Profile.objects.create(user= user)
        self.send_confirmation_email(user)       
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
        user = super(UserSignupSerializer,self).to_representation(instance)
        user.pop('password', None)
        return {
            'user': user,
            'access_token': self.context['token']
        }

#Documentation
class ResponseUserModelSerializer(serializers.Serializer):

    expiry = serializers.CharField()
    user =  UserModelSerializer(many=True, read_only=True)
    token = serializers.CharField()

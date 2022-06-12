#django
from django.contrib.auth import login

#Djano rest framework library
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets,mixins

#Permisos
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)
from portafoliobackend.users.permissions import  (
    IsAccountOwner, 
    IsAccountVerified
)

#Parses
from portafoliobackend.utils.parser import MultipartJsonParser
from rest_framework.parsers import MultiPartParser

#Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

#Serializers
from rest_framework.serializers import Serializer
from portafoliobackend.users.serializers import (
    ProfileModelSerializer,
    BaseProfileModelSerializer
)
from portafoliobackend.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignupSerializer,
    AccountVerificationSerializer,
    ResponseUserModelSerializer,
    ListUserModelSerializer
)

#Models
from portafoliobackend.users.models import Users

#Vistas Know
from knox.views import (
    LogoutAllView,
    LogoutView, 
    LoginView
)
#Documentation
from drf_yasg.utils import swagger_auto_schema

class UserLoginView(LoginView):
    permissions = [
        AllowAny
    ]
    def login(self, request, format=None,*args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(UserViewSet, self).post(request, format)

# > This class is a subclass of the Django Rest Framework's `LogoutView` class. It overrides the
# `permissions` attribute of the `LogoutView` class to include the `IsAccountOwner` permission
class UserLogoutView(LogoutView):

    def logout(self, request, format=None):
        return super().post(request, format)

# > This class is a subclass of the `LogoutAllView` class, and it overrides the `permissions`
# attribute to add the `IsAccountOwner`, `IsAccountVerified`, and `` permissions
class UserLogoutAllView(LogoutAllView):

    def logout_all(self, request, format=None):
        return super().post(request, format)


# It's a viewset that allows you to retrieve, list, and update users.
class UserViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet,
                UserLoginView,
                UserLogoutView,
                UserLogoutAllView):

    #Search users
    queryset = Users.objects.filter(is_active=True)

    #Search user campo
    lookup_field = 'username'

    #Parser
    parser_classes = (MultiPartParser,)
    #Filters
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    search_fields = ('username','firts_name','last_name','email','country',)
    ordering_fields = ('created','username','firts_name')
    ordering = ('created','username')

    def get_permissions(self):
        """
        If the action is profile, then the user must be authenticated, must be the account owner, and
        must have a verified account
        :return: A list of permissions
        """
     
        if self.action in ['profile']:
            permissions = [
                IsAuthenticated, 
                IsAccountOwner,
                IsAccountVerified
            ]
        elif self.action in ['update','partial_update','logout']:
            permissions = [
                IsAuthenticated, 
                IsAccountOwner
            ]
        elif self.action == 'logout-all':
             permissions = [
                IsAuthenticated, 
                IsAccountOwner,
                IsAccountVerified, 
                IsAdminUser
            ]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]

    def get_serializer_class(self):
        """
        If the action is list, return the ListUserModelSerializer, otherwise return the
        UserModelSerializer
        """
        if self.action == 'list':
            return ListUserModelSerializer
        elif self.action in ['retrieve','partial_update','update','list']:
            return UserModelSerializer
        else:
            return Serializer

    # A decorator that is used to document the view.
    @swagger_auto_schema(
        operation_description='Login de usuario, retorna los datos del mismo más el token de authentificación',
        request_body= UserLoginSerializer,
        responses={
            200:ResponseUserModelSerializer
        }
    )
    @action(detail=False,methods=['post'], url_name='login')
    def login(self, request, format=None,*args, **kwargs):
        return super(UserViewSet, self).login(request, format)

    # It's a decorator that is used to document the view.
    @swagger_auto_schema(
        operation_description='Logout user',
        responses={
            204:"Sin contenido"
        }
    )
    @action(detail=False,methods=['post'])
    def logout(self,request, format=None):
        return super(UserViewSet, self).logout(request, format)

    @swagger_auto_schema(
        operation_description='Logout all user',
        responses={
            204:"Sin contenido"
        }
    )
    @action(detail=False,methods=['post'])
    def logout_all(self,request, format=None):
        return super(UserViewSet, self).logout_all(request, format)

    @swagger_auto_schema(
        operation_description='Crear usuario',
        request_body= UserSignupSerializer,
        responses={
            201:ResponseUserModelSerializer
        }
    )
    @action(detail=False,methods=['post'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        login_user = self.login(request)
        return Response(login_user.data, status= status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description='Verificar a un usuario mediante código que llega al correo',
        request_body= AccountVerificationSerializer,
        responses={
            200:UserModelSerializer
        }
    )
    @action(detail=False,methods=['post'])
    def verify(self, request):
        """
        It takes the request data, validates it, saves it, and returns a response
        
        :param request: The request object
        :return: The serializer.data is being returned.
        """
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_200_OK)

    # A decorator that is used to document the view.
    @swagger_auto_schema(
        operation_description='Edición de perfil',
        methods=['put','patch'],
        request_body= BaseProfileModelSerializer,
        responses={
            200:UserModelSerializer
        },
        tags=['Profile'],
    )
    @action(detail=True, methods=['put','patch'])
    def profile(self, request, *args, **kwargs):
        """
        It takes a user object, gets the profile object associated with that user, and then updates the
        profile object with the data from the request
        
        :param request: The request object
        :return: The user object is being returned.
        """
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH' 
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)


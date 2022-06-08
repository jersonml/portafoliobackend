#Djano rest framework library
from re import I
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets,mixins

#Permisos
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)

from portafoliobackend.users.permissions import  IsAccountOwner, IsAccountVerified

#Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

#Serializers
from portafoliobackend.users.serializers import ProfileModelSerializer
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
from knox.views import LogoutAllView,LogoutView

#Documentation
from drf_yasg.utils import swagger_auto_schema


# It's a viewset that allows you to retrieve, list, and update users.
class UserViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    queryset = Users.objects.filter(is_active=True)
    lookup_field = 'username'

    #Filters
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    search_fields = ('username','firts_name','last_name','email','country',)
    ordering_fields = ('created','username','firts_name')
    ordering = ('created','username')

    def get_permissions(self):
        """
        If the action is profile, then the user must be authenticated, must be the account owner, and
        must have a verified account. 
        
        If the action is update or partial_update, then the user must be authenticated and must be the
        account owner. 
        
        Otherwise, the user can be anyone.
        :return: A list of permissions
        """
        if self.action in ['profile']:
            permissions = [
                IsAuthenticated, 
                IsAccountOwner,
                IsAccountVerified
            ]
        elif self.action in ['update','partial_update']:
            permissions = [
                IsAuthenticated, 
                IsAccountOwner
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
        else: 
            return UserModelSerializer

    # A decorator that is used to document the view.
    @swagger_auto_schema(
        operation_description='Login de usuario, retorna los datos del mismo más el token de authentificación',
        request_body= UserLoginSerializer,
        responses={
            200:ResponseUserModelSerializer
        }
    )
    @action(detail=False,methods=['post'])
    def login(self, request):
        """
        It takes a request, validates it, saves it, and returns a response
        
        :param request: The request object is the first parameter to the view. It contains the request
        data, such as the HTTP method, the URL, the headers, the body, and so on
        :return: The serializer.data is being returned.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description='Crear usuario',
        request_body= UserSignupSerializer,
        responses={
            201:UserModelSerializer
        }
    )
    @action(detail=False,methods=['post'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

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
        request_body= ProfileModelSerializer,
        responses={
            200:UserModelSerializer
        },
        tags=['Profile']
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


# > This class is a subclass of the Django Rest Framework's `LogoutView` class. It overrides the
# `permissions` attribute of the `LogoutView` class to include the `IsAccountOwner` permission
class UserLogoutView(LogoutView):
    permissions = [
        IsAuthenticated, 
        IsAccountOwner
    ]


# > This class is a subclass of the `LogoutAllView` class, and it overrides the `permissions`
# attribute to add the `IsAccountOwner`, `IsAccountVerified`, and `` permissions
class UserLogoutAllView(LogoutAllView):
    permissions = [
        IsAuthenticated, 
        IsAccountOwner,
        IsAccountVerified, 
        IsAdminUser
    ]
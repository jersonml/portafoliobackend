#Djano rest framework library
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets,mixins

#Permisos
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from portafoliobackend.users.permissions import IsAccountOwner, IsAccountVerified

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
    ResponseUserModelSerializer
)

#Models
from portafoliobackend.users.models import Users

#Documentation
from drf_yasg.utils import swagger_auto_schema

class UserViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    queryset = Users.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    #Filters
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    search_fields = ('username','firts_name','last_name','email','country',)
    ordering_fields = ('created','username','firts_name')
    ordering = ('created','username')

    def get_permissions(self):
        if self.action in ['signup','login','verify']:
            permissions = [AllowAny]
        elif self.action == ['update','partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner,IsAccountVerified]
        elif self.action == ['retrieve']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @swagger_auto_schema(
        operation_description='Login de usuario, retorna los datos del mismo más el token de authentificación',
        request_body= UserLoginSerializer,
        responses={200:ResponseUserModelSerializer}
    )
    @action(detail=False,methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user,token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status= status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def verify(self, request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulation,Welcome!',
        }
        return Response(data, status= status.HTTP_200_OK)

    @action(detail=True, methods=['put','patch'])
    def profile(self, request, *args, **kwargs):
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

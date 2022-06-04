from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets,mixins

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from portafoliobackend.users.permissions import IsAccountOwner


from portafoliobackend.circles.serializers import CircleModelSerializer
from portafoliobackend.users.serializers import ProfileModelSerializer
from portafoliobackend.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignupSerializer,
    AccountVerificationSerializer
)
from portafoliobackend.users.models import Users
from portafoliobackend.circles.models import Circle

class UserViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    queryset = Users.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['signup','login','verify']:
            permissions = [AllowAny]
        elif self.action == ['retrieve','update','partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]


    @action(detail=False,methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user,token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status= status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
        }
        return Response(data, status= status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def verify(self, request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulation,now go share somo rides!',
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


    def retrieve(self, request, *args, **kwargs):
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members= request.user,
            membership__is_active = True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response 
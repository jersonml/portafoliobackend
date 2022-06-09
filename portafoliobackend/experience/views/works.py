#Django
from django.shortcuts import get_object_or_404

#Djano rest framework library
from rest_framework import viewsets,mixins

#Permisos
from portafoliobackend.users.permissions import (
    IsAccountOwner, 
    IsAccountVerified
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
#Authentication
from knox.auth import TokenAuthentication

#Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

#Serializers
from portafoliobackend.experience.serializers import WorksModelSerializer

#Parses
from drf_nested_field_multipart import NestedMultipartParser

#Models
from portafoliobackend.users.models import Profile, Users
from portafoliobackend.experience.models import Works

#Documentation
from drf_yasg.utils import swagger_auto_schema

# It's a viewset that allows you to create, list, update and retrieve courses
class WorksViewSet(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):

    #Serializer
    serializer_class = WorksModelSerializer
    #url param
    lookup_field = 'slug_name'
    #permission and authentification
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsAccountOwner,IsAccountVerified]

    parser_classes = (NestedMultipartParser,)

    #Filters
    filter_backends = (SearchFilter, OrderingFilter,DjangoFilterBackend)
    search_fields = ('name','position','date_end')
    ordering_fields = ('date_end','position')
    ordering = ('date_end')

    #tags documentation
    my_tags = ["Works"]


    def dispatch(self, request, *args, **kwargs):
        """
        It takes the username from the URL and uses it to get the user object from the database
        
        :param request: The request object
        :return: The super class is being returned.
        """
        username = kwargs['username']
        self.user = get_object_or_404(Users, username=username)
        return super(WorksViewSet,self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        It returns all the courses that the user is enrolled in
        :return: The courses that the user is enrolled in.
        """
        if getattr(self, "swagger_fake_view", False):
            return Works.objects.none()

        profile: Profile = self.user.profile
        return profile.works.all()

    """def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()"""
        
    def get_permissions(self):
        if self.action in ['create','update','partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner, IsAccountVerified]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        The function takes in a serializer, saves it, and then adds the course to the profile of the
        user who created it
        
        :param serializer: The serializer instance that should be used for validating and
        """
        course = serializer.save()
        profile: Profile = self.user.profile
        profile.works.add(course)
  
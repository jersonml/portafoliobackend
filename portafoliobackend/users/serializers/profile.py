#Django Rest Framework
from rest_framework import serializers

#Serializers
from portafoliobackend.experience.serializers import CoursesModelSerializer
from portafoliobackend.experience.serializers import ItemsModelSerializer
from portafoliobackend.experience.serializers import WorksModelSerializer
from portafoliobackend.socialnetworks.serializers import SocialNetworksModelSerializer

#Models
from portafoliobackend.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):

    courses = CoursesModelSerializer(many=True)
    social_networks = SocialNetworksModelSerializer(many=True)
    items = ItemsModelSerializer(many=True)
    works = WorksModelSerializer(many=True)

    #experience = serializers.SerializerMethodField()

    class Meta:

        model = Profile
        fields = (
            'courses',
            'social_networks',
            'items',
            'works',
            'picture',
            'resume',
            'biography',
            'level_academy',
            'qualities',
            'experience'
        )
        read_only_fields = (
            'courses',
            'social_networks',
            'items',
            'works'
        )
        

    """def get_experience(self, obj):
        return {
            'years':obj.experience.total_minutes
        }"""


class ListProfileModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile
        fields = (
            'picture',
            'resume',
            'biography',
            'level_academy',
            'qualities',
            'experience'
        )

      
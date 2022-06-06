from rest_framework import serializers

from portafoliobackend.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):

    #courses = CoursesModelSerializer()
    #social_networks = SocialNetworksModelSerializer()
    #items = ItemsModelSerializer()
    #works = WorksModelSerializer()

    class Meta:

        model = Profile
        exclude= ['id', 'created','modified','user']
      
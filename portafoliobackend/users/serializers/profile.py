from rest_framework import serializers

from portafoliobackend.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile
        fields= (
            'picture',
            'biography',
        )
      
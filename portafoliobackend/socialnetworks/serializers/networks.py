from rest_framework import serializers

from portafoliobackend.socialnetworks.models import SocialNetworks

class SocialNetworksModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = SocialNetworks
        exclude= ['id', 'created','modified']
      
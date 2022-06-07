from rest_framework import serializers

from portafoliobackend.experience.models import Items

class ItemsModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Items
        exclude= ['id', 'created','modified']
      
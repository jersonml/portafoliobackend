from rest_framework import serializers

from portafoliobackend.experience.models import Works
from portafoliobackend.experience.serializers import ItemsModelSerializer

class WorksModelSerializer(serializers.ModelSerializer):

    tags = ItemsModelSerializer()

    class Meta:

        model = Works
        exclude= ['id', 'created','modified']
      
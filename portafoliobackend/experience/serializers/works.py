#Django Rest Framework
from rest_framework import serializers

#Models
from portafoliobackend.experience.models import Works, Items


from portafoliobackend.experience.serializers import ItemsModelSerializer

class WorksModelSerializer(serializers.ModelSerializer):

    tags = ItemsModelSerializer(many=True)

    class Meta:

        model = Works
        fields = [
            'tags',
            'constancy',
            'capture',
            'name',
            'rif',
            'position',
            'description',
            'link',
            'date_init',
            'date_end'
        ]
      
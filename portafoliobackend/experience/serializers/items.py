from rest_framework import serializers

from portafoliobackend.experience.models import Items

class ItemsModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Items
        fields = [
            'name',
            'category',
            'slug_name',
            'sub_category',
            'description',
            'leve',
            'experience'
        ]
      
#Django Rest Framework
from rest_framework import serializers

#Serializers
from portafoliobackend.experience.serializers.items import ItemsModelSerializer

#Models
from portafoliobackend.experience.models import Works
from portafoliobackend.experience.models.items import Items

class WorksModelSerializer(serializers.ModelSerializer):

    item_id = serializers.ListField(
        child= serializers.IntegerField(), 
        write_only=True,
        allow_empty=True

    )
    tags = ItemsModelSerializer(read_only=True, many=True)

    class Meta:

        model = Works
        fields = [
            'item_id',
            'tags',
            'slug_name',
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
        
    def validate_tags(self,id_item):
        try:
            item = Items.objects.get(pk=id_item)
        except Items.DoesNotExist:
            raise serializers.ValidationError('Invalid items.')

        self.context['item'] = item

        return id_item

    def create(self, validated_data):
        return super().create(validated_data)
    
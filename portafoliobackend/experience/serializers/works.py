#Django Rest Framework
from rest_framework import serializers

#Models
from portafoliobackend.experience.models import Works
from portafoliobackend.experience.models.items import Items

class WorksModelSerializer(serializers.ModelSerializer):

    tags = serializers.IntegerField(write_only=True)

    class Meta:

        model = Works
        fields = [
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
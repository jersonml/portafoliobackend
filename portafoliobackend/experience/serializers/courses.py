from attr import fields
from rest_framework import serializers

from portafoliobackend.experience.models import Courses

class CoursesModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Courses
        fields = [
            'name',
            'category',
            'sub_category',
            'plataform',
            'picture',
            'certificate',
            'leve',
            'date_approved'
        ]
      
#Library
from datetime import timedelta

#Django Rest Framework
from rest_framework import serializers

#Serializers
from portafoliobackend.experience.serializers import CoursesModelSerializer
from portafoliobackend.experience.serializers import ItemsModelSerializer
from portafoliobackend.experience.serializers import WorksModelSerializer
from portafoliobackend.socialnetworks.serializers import SocialNetworksModelSerializer

#Models
from portafoliobackend.users.models import Profile

class BaseProfileModelSerializer(serializers.ModelSerializer):

    experience = serializers.SerializerMethodField()
    experience_date = serializers.JSONField(
        write_only= True,
        required= False,
        help_text = "example: {'years':4,'month':1,'week':3}"
    )

    class Meta:

        model = Profile
        fields = (
            'picture',
            'resume',
            'biography',
            'level_academy',
            'qualities',
            'experience',
            'experience_date'
        )

    def get_experience(self,obj):
        if isinstance(obj.experience, timedelta):
                
            days = obj.experience.days
            years, days = divmod(days, 365)
            month, days = divmod(days, 30)
            week, _ = divmod(days, 7)
        else:
            years = month = week = 0
        return  {
            'years': years,
            'month': month,
            'week': week 
        }

class ProfileModelSerializer(BaseProfileModelSerializer):

    DATE_EXPERIENCE = [
        'years',
        'month',
        'week'
    ]

    courses = CoursesModelSerializer(many=True)
    social_networks = SocialNetworksModelSerializer(many=True)
    items = ItemsModelSerializer(many=True)
    works = WorksModelSerializer(many=True)


    class Meta(BaseProfileModelSerializer.Meta):

        fields = (
            'courses',
            'social_networks',
            'items',
            'works',
            'picture',
            'resume',
            'biography',
            'level_academy',
            'qualities',
            'experience',
            'experience_date'
        )
        read_only_fields = (
            'courses',
            'social_networks',
            'items',
            'works'
        )


    def validate_experience_date(self, attrs):
        if  attrs:

            required = set(self.DATE_EXPERIENCE) - set(attrs.keys())
            if required:
                raise serializers.ValidationError(f'required add key experience: {required}')
            
            days = attrs['years']*365
            days += attrs['month']*30
            days += attrs['week']*7

            return {'time':timedelta(days=days)}
        else:
            return attrs
    
    
    def update(self, instance, validated_data):
        validated_data['experience'] = validated_data['experience_date'].get('time')
        return super().update(instance, validated_data)




      
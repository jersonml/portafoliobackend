#Serializer extract choices
from typing import List, Tuple
from portafoliobackend.users.models import Users


class CurrentUsersItemsDefault:
    requires_context = True

    def __call__(self, serializer_field):
        #User
        user: Users = serializer_field.context['request'].user
        #Choices items users
        choices_deault: List[Tuple[int,str]] = \
            user.profile.items.all().values_list('id','name')
            
        return [(1,2)]

    def __repr__(self):
        return '%s()' % self.__class__.__name__
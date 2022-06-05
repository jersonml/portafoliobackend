#Django
from django.db import models

#Models
from portafoliobackend.utils.models import MasterModel

class SocialNetworks(MasterModel):
    """ Modelo que representa la experiencia en los trabajo
        del usuario. Hereda del modelo master 
    """
    #Constante
    NETWORKS_CHOICE = [
        (1,'Facebook'),
        (2,'Instagram'),
        (3, 'LinkedIn'),
        (4, 'Twitter'),
        (5, 'WhatsApp'),
        (6, 'YouTube')
    ]

    #Text
    type_network = models.CharField(
        max_length=20,
        choices= NETWORKS_CHOICE
    )
    
    #URL
    link =  models.URLField( max_length=250 )
   
    def __str__(self):
        return str(self.type_network)
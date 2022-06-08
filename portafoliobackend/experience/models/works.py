#Django
from distutils.command.upload import upload
from django.db import models

#Models
from portafoliobackend.utils.models import MasterModel

class Works(MasterModel):
    """ Modelo que representa la experiencia en los trabajo
        del usuario. Hereda del modelo master 
    """

    #Relations
    tags = models.ManyToManyField('experience.Items')

    #Field
    constancy = models.FileField(
        'constancy work',
        upload_to='users/work/',
        blank = True,
        null = True
    )
    capture = models.ImageField(
        'Capture work constance',
        upload_to = 'users/work/img/',
        blank = True,
        null = True
    )
    
    #Text
    name = models.CharField(
        max_length=50,
        help_text= "Nombre de la empresa donde se trabajó, ejemplo: Platzi"
    )
    rif = models.CharField(
        max_length=30,
        help_text= "Identificación de la empresa",
        blank=True
    )
    position = models.CharField(
        max_length=30,
        help_text= "Identificación de la empresa"
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        help_text= "nombre de la plataforma, ejemplo: platzi"
    )
    
    #URL
    link =  models.URLField( max_length=150 )
   
    #Date
    date_init = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return str(self.name)
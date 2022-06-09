#Django
from django.db import models

#Models
from portafoliobackend.utils.models import MasterModel

#Manager
from portafoliobackend.experience.managers import SlugNameManager

class   Items(MasterModel):
    """ Modelo que contiene los items del lenguaje
        de programación que maneja Hereda del modelo master 
    """
    #Constante
    LEVEL_CHOICE = [
        (1,'Básico'),
        (2,'Intermedio'),
        (3, 'Avanzado')
    ]

    #Text
    name = models.CharField(
        max_length=50,
        help_text= "Nombre del lenguaje de programación, ejemplo: Python "
    )
    category = models.CharField(
        max_length=30,
        help_text= "category, ejemplo: Backend, Ingles, Froned"
    )
    slug_name = models.SlugField(
        unique=True,
        max_length=40
    )
    sub_category = models.CharField(
        max_length=30,
        help_text= "sub Categoría del item, ejemplo: Django"
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        help_text= "nombre de la plataforma, ejemplo: platzi"
    )
    
    #Int
    leve = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICE,
        help_text="Dificultad del curso"
    )

    #Date
    experience = models.DurationField(
        blank=True,
        null= True,
        help_text= "Experience of items"
    )

    #manager
    objects = SlugNameManager

    def __str__(self):
        return str(self.name)
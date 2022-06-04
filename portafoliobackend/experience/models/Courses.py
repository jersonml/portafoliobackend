#Django
from django.db import models

#Models
from portafoliobackend.utils.models import MasterModel

class Courses(MasterModel):
    """ Modelo que contiene los cursos que realizo el usuario,
        Hereda del modelo master 
    """
    #Constante
    LEVEL_CHOICE = [
        (1,'Básico'),
        (2,'Intermedio'),
        (3, 'Avanzado')
    ]

    #Text
    name = models.CharField(
        min_length=3, 
        max_length=50,
        help_text= "Nombre del curso, ejemplo: Python profesional"
    )
    category = models.CharField(
        min_length=3, 
        max_length=30,
        help_text= "Categoría del curso, ejemplo: Backend"
    )
    sub_category = models.CharField(
        min_length=3, 
        max_length=30,
        help_text= "sub Categoría del curso, ejemplo: Python"
    )
    plataform = models.TextField(
        min_length=5, 
        max_length=50,
        blank=True,
        null=True,
        help_text= "nombre de la plataforma, ejemplo: platzi"
    )

    #Files
    picture = models.ImageField(
        'profile picture',
        upload_to= 'course/',
        blank = True,
        null= True 
    )
    certificate = models.FieldFile(
        'Resume users',
        upload_to='users/certificate/',
        blank = True,
        null = True
    )
    
    #Int
    leve = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICE,
        help_text="Dificultad del curso"
    )

    #Date
    date_approved = models.DateTimeField()

    def __str__(self):
        return str(self.user)
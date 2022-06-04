#Django
from django.db import models

#Models
from portafoliobackend.utils.models import MasterModel

class Profile(MasterModel):
    """ Modelo que contiene los datos de perfin de un usuario,
        Hereda del modelo master y del modelo por deault
        de django. Modelo que hace todas las relaciones

    """

    #Relations
    user = models.OneToOneField('users.Users', on_delete=models.CASCADE)
    courses = models.ManyToManyField('experience.Courses', on_delete= models.CASCADE)
    social_networks = models.ManyToManyField('socialnetworks.SocialNetworks', on_delete= models.CASCADE)
    items = models.ManyToManyField('experience.Items', on_delete=models.CASCADE)
    work = models.ManyToManyField('experience.Work', on_delete=models.CASCADE)

    #Files
    picture = models.ImageField(
        'profile picture',
        upload_to= 'users/pictures/',
        blank = True,
        null= True 
    )
    resume = models.FieldFile(
        'Resume users',
        upload_to='users/resume/',
        blank = True,
        null = True
    )

    #Text
    biography = models.TextField(
        max_length=500, 
        blank=True,
        help_text="Descripción del usuario"
    )
    level_academy = models.TextField(
        max_length=400, 
        blank=True,
        help_text= "Nivel académico que posee el usuario"
    )
    qualities = models.TextField(
        max_length=400,
        blank=True,
        help_text="Cualidades del usuario"
    )

    years_experience = models.DateTimeField()

    def __str__(self):
        return str(self.user)
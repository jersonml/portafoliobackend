#Model users 

#utils
from json import load
from pyexpat import model

#Django library
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

#Models
from portafoliobackend.utils.models import MasterModel

class Users(MasterModel, AbstractUser):
    """ Modelo que contiene los datos de un usuario,
        Hereda del modelo master y del modelo por deault
        de django 

    """
    #CONSTANTE
    DEFAULT_COUNTRIE = "VE"
    
    #Se leen todos os países
    with open('portafoliobackend/utils/data/countries.json') as f:
        data = load(f)

    COUNTRIES_CHOICE = [(x['code'],x['name_es']) for x in data['countries']]

    email = models.EmailField(
        'email address',
        unique= True,
        error_messages={
            'unique': 'A user with that email already exists'
        }
    )

    phone_regex= RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999 up to 15 digits allowed"
    )

    phone_number= models.CharField(
        max_length=17, 
        blank=True, 
        validators=[phone_regex]
    )

    country = models.CharField(
        max_length=2,
        choices= COUNTRIES_CHOICE,
        default= DEFAULT_COUNTRIE,
        help_text="Seleccionar país"
    )

    is_verify = models.BooleanField(
        'verify users',
        default= False
    )

    def __str__(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return self.username

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
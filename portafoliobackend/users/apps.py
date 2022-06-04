from django.apps import AppConfig

class UsersAppConfig(AppConfig):

    default_auto_field = 'django.db.models.AutoField'
    name = 'portafoliobackend.users'
    verbose_name: str = 'Users'
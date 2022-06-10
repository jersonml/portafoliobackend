#Django
from django.urls import path, include

#Django Rest Frameworks
from rest_framework.routers import DefaultRouter

#Vistas
from .views import users as user_views

router = DefaultRouter()
router.register(r'users',user_views.UserViewSet, basename='user')

urlpatterns = router.urls
app_name = 'api'
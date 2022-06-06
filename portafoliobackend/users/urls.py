#Django
from django.urls import path, include

#Django Rest Frameworks
from rest_framework.routers import DefaultRouter

#Vistas
from .views import users as user_views
from knox import views as knox_views

router = DefaultRouter()
router.register(r'users',user_views.UserViewSet, basename='users')

urlpatterns = [
    path('',include(router.urls)),
    path('users/logout/',knox_views.LogoutView.as_view(), name="knox-logout"),
    path('users/logoutall/',knox_views.LogoutAllView.as_view(), name="knox-logoutall")
]
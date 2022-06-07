#Django
from django.urls import path, include

#Django Rest Frameworks
from rest_framework.routers import DefaultRouter

#Vistas
from .views import users as user_views

router = DefaultRouter()
router.register(r'users',user_views.UserViewSet, basename='users')

urlpatterns = [
    path('',include(router.urls)),
    path('users/logout/',user_views.UserLogoutAllView.as_view(), name="knox-logout"),
    path('users/logoutall/',user_views.UserLogoutAllView.as_view(), name="knox-logoutall")
]
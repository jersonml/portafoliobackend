#Django
from django.urls import path, include

#Django Rest Frameworks
from rest_framework.routers import DefaultRouter

#Vistas
from .views import courses as course_views

router = DefaultRouter()
router.register(
    r'users/(?P<username>[-a-zA-Z0-0_]+)/profile/courses',
    course_views.CoursesViewSet, 
    basename='courses'
)

urlpatterns = [
    path('',include(router.urls)),
]


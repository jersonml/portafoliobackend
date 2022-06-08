#Django
from django.urls import path, include

#Django Rest Frameworks
from rest_framework.routers import DefaultRouter

#Vistas
from .views import courses as course_views
from .views import items as item_views
from .views import works as work_views

router = DefaultRouter()
router.register(
    r'users/(?P<username>[-a-zA-Z0-0_]+)/profile/courses',
    course_views.CoursesViewSet, 
    basename='courses'
)
router.register(
    r'users/(?P<username>[-a-zA-Z0-0_]+)/profile/items',
    item_views.ItemsViewSet, 
    basename='items'
)
router.register(
    r'users/(?P<username>[-a-zA-Z0-0_]+)/profile/works',
    work_views.WorksViewSet, 
    basename='works'
)

urlpatterns = [
    path('',include(router.urls)),
]


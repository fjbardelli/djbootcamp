from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personas.views import AlumnosViewSet, DocentesViewSet, CoordinadoresViewSet


router = DefaultRouter() # trailing_slash=False
router.register(r'alumnos', AlumnosViewSet, basename='alumnos')
router.register(r'docentes', DocentesViewSet, basename='docentes')
router.register(r'coordinadores', CoordinadoresViewSet, basename='coordinadores')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from comisiones.views import ComisionViewSet, ComisionAlumnosViewSet


router = DefaultRouter()
router.register(r'comisiones', ComisionViewSet, basename='comisiones')
router.register(r'inscripciones', ComisionAlumnosViewSet, basename='inscripciones')

urlpatterns = [
    path('', include(router.urls)),
]
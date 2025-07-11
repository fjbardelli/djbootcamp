from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materias.views import MateriaViewSet


router = DefaultRouter()
router.register(r'materias', MateriaViewSet, basename='materias')

urlpatterns = [
    path('', include(router.urls)),
]
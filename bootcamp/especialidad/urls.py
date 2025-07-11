from django.urls import path, include
from rest_framework.routers import DefaultRouter
from especialidad.views import EspecialidadViewSet


router = DefaultRouter()
router.register(r'especialidad', EspecialidadViewSet, basename='especialidad')

urlpatterns = [
    path('', include(router.urls)),
]
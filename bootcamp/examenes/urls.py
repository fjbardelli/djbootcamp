from django.urls import path, include
from rest_framework.routers import DefaultRouter
from examenes.views import ExamenViewSet


router = DefaultRouter()
router.register(r'examenes', ExamenViewSet, basename='examenes')


urlpatterns = [
    path('', include(router.urls)),
]
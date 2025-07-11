from django.shortcuts import render
from rest_framework import viewsets
from .models import Especialidad
from .serializer import EspecialidadSerializer
from .permissions import IsCoordinadorOrAdmin

# Create your views here.

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [IsCoordinadorOrAdmin]

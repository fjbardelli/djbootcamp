from django.shortcuts import render
from rest_framework import viewsets
from materias.models import Materia
from materias.serializer import MateriaSerializer
from materias.permissions import IsCoordinadorOrAdmin

# Create your views here.

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsCoordinadorOrAdmin]

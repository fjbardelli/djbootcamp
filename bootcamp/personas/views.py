from rest_framework import viewsets
from personas.models import Alumno, Docente, Coordinador
from personas.serializer import AlumnoSerializer, DocenteSerializer, CoordinadorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from personas.permissions import IsCoordinadorOrAdmin, IsCoordinadorOrDocenteOrAdmin


class CoordinadoresViewSet(viewsets.ModelViewSet):
    queryset = Coordinador.objects.all()
    serializer_class = CoordinadorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def activos(self, request):
        paginator = self.pagination_class()
        activos = Coordinador.objects.activos()
        page = paginator.paginate_queryset(activos, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        inactivos = Coordinador.objects.inactivos()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(inactivos, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class DocentesViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()
    serializer_class = DocenteSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsCoordinadorOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def activos(self, request):
        activos = Docente.objects.activos()
        serializer = self.get_serializer(activos, many=True)
        pagination_class = self.pagination_class
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        inactivos = Docente.objects.inactivos()
        serializer = self.get_serializer(inactivos, many=True)
        return Response(serializer.data)

class AlumnosViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsCoordinadorOrDocenteOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def activos(self, request):
        activos = Alumno.objects.activos()
        serializer = self.get_serializer(activos, many=True)
        pagination_class = self.pagination_class
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        inactivos = Alumno.objects.inactivos()
        serializer = self.get_serializer(inactivos, many=True)
        return Response(serializer.data)
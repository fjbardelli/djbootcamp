from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime
from utils import DRFResponse
from comisiones.services import ComisionService, ComisionEmailService
from comisiones.models import Comision, ComisionAlumnos
from comisiones.serializer import ComisionSerializer, ComisionAlumnosSerializer


# Create your views here.

class ComisionViewSet(viewsets.ModelViewSet):
    queryset = Comision.objects.all()
    serializer_class = ComisionSerializer

    def create(self, request, *args, **kwargs):

        inicio = datetime.strptime(request.data.get('fecha_inicio'), '%Y-%m-%d').date()
        fin = datetime.strptime(request.data.get('fecha_fin'), '%Y-%m-%d').date()

        try:
            comision_service = ComisionService(ComisionEmailService)
            comision:Comision = comision_service.crear_comision(
                materia=request.data.get('materia'),
                docente=request.data.get('docente'),
                inicio=inicio,
                fin=fin,
                nombre=request.data.get('nombre'),
                horario=request.data.get('horario'),
                aula=request.data.get('aula')
            )
            return DRFResponse.created(message='Comisión creada exitosamente.',
                                data=self.serializer_class(comision).data)

        except Exception as e:
            print("\n\n\n\n", e)
            return DRFResponse.error(message="La Comision no ha sido creada.")

class ComisionAlumnosViewSet(viewsets.ModelViewSet):
    queryset = ComisionAlumnos.objects.all()
    serializer_class = ComisionAlumnosSerializer

    @action(detail=True, methods=['get'])
    def listado(self, request,  pk=None):
        pk = int(pk)
        alumnos = ComisionAlumnos.objects.filter(comision=pk).select_related('alumno').order_by('alumno__apellido', 'alumno__nombre')
        serializer = self.get_serializer(alumnos, many=True)
        self.pagination_class = self.pagination_class
        return Response(serializer.data)
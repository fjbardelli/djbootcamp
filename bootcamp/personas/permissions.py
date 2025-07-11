from rest_framework import permissions
from personas.models import Coordinador, Docente, Alumno, Persona

class IsCoordinadorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        coordinador = Coordinador.objects.filter(user=request.user).first()
        if coordinador:
            return True
        else:
            if request.user.is_staff:
                return True
        return False

class IsCoordinadorOrDocenteOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        coordinador = Coordinador.objects.filter(user=request.user).first()
        if coordinador:
            return True
        docente = Docente.objects.filter(user=request.user).first()
        if docente:
            return True
        elif request.user.is_staff:
                return True
        return False
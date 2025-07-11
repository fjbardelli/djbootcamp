from rest_framework import permissions
from personas.models import Coordinador, Docente, Alumno, Persona

class IsCoordinadorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):

        if view.action in ['list', 'retrieve']:
            return True
        coordinador = Coordinador.objects.filter(user=request.user).first()
        if coordinador:
            return True
        else:
            if request.user.is_staff:
                return True
        return False
from django.db import models

class CoordinadoresManager(models.Manager):
    def activos(self):
        return super().get_queryset().filter(activo=True)

    def inactivos(self):
        return super().get_queryset().filter(activo=False)
class AlumnoManager(models.Manager):
    def activos(self):
        return super().get_queryset().filter(activo=True)

    def inactivos(self):
        return super().get_queryset().filter(activo=False)

class DocenteManager(models.Manager):
    def activos(self):
        return super().get_queryset().filter(activo=True)

    def inactivos(self):
        return super().get_queryset().filter(activo=False)
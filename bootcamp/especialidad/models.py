from django.db import models
from especialidad.manager import EspecialidadManager

class Especialidad(models.Model):

    nombre = models.CharField(max_length=100,blank=False, null=False, default=None)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['descripcion']

    objects = EspecialidadManager()

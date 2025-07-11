from django.db import models


class Examen(models.Model):

    temario = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)
    comision = models.OneToOneField("comisiones.Comision", on_delete=models.CASCADE, related_name='examen')

    def __str__(self):
        return f"{self.comision} - {self.fecha} {self.hora_inicio}"



from django.db import models

class Materia(models.Model):

    nombre = models.CharField(max_length=100, blank=False, null=False)
    codigo = models.CharField(max_length=20, unique=True, blank=False, null=False)
    creditos = models.PositiveIntegerField(default=100, blank=False, null=False)
    semestre = models.PositiveIntegerField(default=1, blank=False, null=False)
    descripcion = models.TextField(blank=True, null=True)
    especialidad = models.ForeignKey (
        'especialidad.Especialidad',
        on_delete=models.DO_NOTHING,
        related_name='especialidad',
        blank=False,
        null=False
    )
    activa = models.BooleanField(default=True, blank=False, null=False)
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['nombre']
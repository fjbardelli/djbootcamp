from django.db import models
 

class DiaSemana(models.TextChoices):
    LUNES = ('LU', 'Lunes')
    MARTES = ('MA', 'Martes')
    MIERCOLES = ('MI', 'Miércoles')
    JUEVES = ('JU', 'Jueves')
    VIERNES = ('VI', 'Viernes')
    SABADO = ('SA', 'Sábado')
    DOMINGO = ('DO', 'Domingo')

class Comision(models.Model):

    nombre = models.CharField(max_length=100, blank=False, null=False)
    fecha_inicio = models.DateField(blank=False, null=False)
    fecha_fin = models.DateField(blank=False, null=False)
    activo = models.BooleanField(default=True)
    docente = models.ForeignKey(
        'personas.Docente',
        on_delete=models.CASCADE,
        related_name='com_docente',
        blank=False,
        null=False
    )
    materia = models.ForeignKey(
        'materias.Materia',
        on_delete=models.DO_NOTHING,
        related_name='com_materia',
        blank=False,
        null=False
    )
    horario = models.CharField(
        max_length=2,
        choices=DiaSemana.choices,
        blank=True,
        null=True
    )
    aula = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Comisión'
        verbose_name_plural = 'Comisiones'
        ordering = ['fecha_inicio', 'nombre']

class ComisionAlumnos (models.Model):
    comision = models.ForeignKey(
        'comisiones.Comision',
        on_delete=models.CASCADE,
        related_name='alumnos',
        blank=False,
        null=False
    )
    alumno = models.ForeignKey(
        'personas.Alumno',
        on_delete=models.DO_NOTHING,
        related_name='comisiones',
        blank=False,
        null=False
    )

    regular = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.comision} - {self.alumno}'

    class Meta:
        verbose_name = 'Comisión Alumno'
        verbose_name_plural = 'Comisiones Alumnos'
        ordering = ['comision', 'alumno']

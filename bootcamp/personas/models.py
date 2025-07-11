from django.db import models
from personas.managers import AlumnoManager, DocenteManager, CoordinadoresManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Persona(models.Model):
    ROLES = [
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
        ('coordinador', 'Coordinador'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True, unique=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='alumno')

    @property
    def nombre_completo(self):
        return f"{self.apellido}, {self.nombre}"

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

    class Meta:
        abstract = True

class Coordinador(Persona):


    objects = CoordinadoresManager()
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = "Coordinador"
        verbose_name_plural = "Coordinadores"
        ordering = ['apellido', 'nombre']

class Docente(Persona, models.Model):

    fecha_contratacion = models.DateField(auto_now_add=True)
    especialidad = models.ForeignKey (
        'especialidad.Especialidad',
        on_delete=models.DO_NOTHING,
        related_name='doc_especialidad',
        blank=False,
        null=False,
        default=1
    )

    objects = DocenteManager()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Alumno(Persona):

    fecha_nacimiento = models.DateField(blank=True, null=True)

    objects  = AlumnoManager()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['apellido', 'nombre']



    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"
        ordering = ['apellido', 'nombre']


# Signals

@receiver(post_save, sender=Alumno)
@receiver(post_save, sender=Docente)
@receiver(post_save, sender=Coordinador)
def crear_usuario(sender, instance, created, **kwargs):
    if created:
        username = instance.nombre.lower() + instance.apellido.lower()
        password = 'password_123'  # generar una contraseña aleatoria aquí
        user = User.objects.create_user(username=username, password=password)
        instance.user = user
        if isinstance(instance, Alumno):
            instance.rol = 'alumno'
        elif isinstance(instance, Docente):
            instance.rol = 'docente'
        elif isinstance(instance, Coordinador):
            instance.rol = 'coordinador'
        instance.save()
        # Enviar un correo electrónico al usuario con sus credenciales
        print(f"Usuario creado: {username}, Contraseña: {password}")

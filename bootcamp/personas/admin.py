from django.contrib import admin
from personas.models import Alumno, Docente

class AlumnoAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'activo')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('activo',)
    ordering = ('apellido', 'nombre')

class DocenteAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'apellido', 'email', 'telefono', 'activo')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('activo',)
    ordering = ('apellido', 'nombre')

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Docente, DocenteAdmin)

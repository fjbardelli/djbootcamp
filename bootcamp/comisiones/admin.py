from django.contrib import admin
from comisiones.models import Comision

class ComisionAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'docente', 'materia', 'activo')
    search_fields = ('nombre', 'docente__nombre', 'materia__nombre')
    list_filter = ('activo', 'materia')
    ordering = ('fecha_inicio', 'nombre')

admin.site.register(Comision, ComisionAdmin)

from django.contrib import admin
from examenes.models import Examen
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('comision__nombre', 'fecha', 'activo')
    search_fields = ('comision__nombre', 'comision__nombre')
    list_filter = ('activo', 'comision__nombre')
    ordering = ('fecha', 'comision__nombre')


admin.site.register(Examen, ExamenAdmin)

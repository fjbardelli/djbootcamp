from django.contrib import admin
from materias.models import Materia

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activa')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activa',)
    ordering = ('nombre',)

admin.site.register(Materia, MateriaAdmin)

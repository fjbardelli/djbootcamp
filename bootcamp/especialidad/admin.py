from django.contrib import admin
from especialidad.models import Especialidad

class EspecialidadAdmin(admin.ModelAdmin):

    list_display = ('descripcion', 'activo')
    search_fields = ('descripcion',)
    list_filter = ('activo',)
    ordering = ('descripcion',)

admin.site.register(Especialidad, EspecialidadAdmin)
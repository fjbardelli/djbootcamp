from django.db import models

class EspecialidadManager(models.Manager):
    def activas(self):
        return super().get_queryset().filter(activo=True)

    def inactivas(self):
        return super().get_queryset().filter(activo=False)

    def todas(self):
        return super().get_queryset()
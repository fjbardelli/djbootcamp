from rest_framework import serializers
from materias.models import Materia

class MateriaSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['especialidad_nombre'] = instance.especialidad.nombre
        return representation

    class Meta:
        model = Materia
        fields = '__all__'

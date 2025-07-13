from rest_framework import serializers
from examenes.models import Examen

class ExamenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Examen
        fields = '__all__'

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['comision_nombre'] = instance.comision.nombre
        representation['materia_nombre'] = instance.comision.materia.nombre
        representation['docente_nombre'] = instance.comision.docente.nombre_completo
        return representation

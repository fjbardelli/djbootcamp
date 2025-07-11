from rest_framework import serializers
from personas.models import Alumno, Docente, Coordinador

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'
        
class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'
        
class CoordinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinador
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = instance.user.username if instance.user else None
        return representation

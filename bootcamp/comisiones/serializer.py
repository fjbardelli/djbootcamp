from rest_framework import serializers
from comisiones.models import Comision, ComisionAlumnos

class ComisionSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['docente'] = instance.docente.nombre_completo
        data['materia'] = instance.materia.nombre
        #data['alumnos'] = [alumno.nombre_completo() for alumno in instance.alumnos.all()]
        return data
    class Meta:
        model = Comision
        fields = '__all__'


class ComisionAlumnosSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id_alumno'] = instance.alumno.pk
        data['alumno'] = instance.alumno.nombre_completo
        data['regular'] = instance.regular
        data['email'] = instance.alumno.email
        return data

    class Meta:
        model = ComisionAlumnos
        fields = '__all__'
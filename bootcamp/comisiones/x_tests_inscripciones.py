from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from comisiones.models import Comision, ComisionAlumnos
from personas.models import Coordinador, Docente, Alumno
from materias.models import Materia
from especialidad.models import Especialidad
from materias.models import Materia
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64
import pdb


data_inscripcion = {
	"comision": 1,
    "alumno": 1
}

class MateriasViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test_user', 'testuser@example.com', 'password')
        self.staff = User.objects.create_user('staff_user', 'staff@example.com', 'password'
                                            , is_staff=True)
        self.especialidad = Especialidad.objects.create(nombre="Especialidad Test",
                                                        descripcion="Descripción Test")
        self.docente = Docente.objects.create(
            nombre="Test",
            apellido="Docente",
            email="docente@bootcamp.com",
            especialidad=self.especialidad
        )
        self.materia = Materia.objects.create(
            nombre = "Historia",
            codigo = "HIS01",
            especialidad = self.especialidad,
            creditos = "100",
            descripcion = "Roma",
            activa = True
        )
        self.alumno = Alumno.objects.create(
            nombre="Test",
            apellido="Alumno",
            email="alumno@bootcamp.com",
        )
        self.comision = Comision.objects.create(
            nombre="Django Intermedio",
            fecha_inicio="2025-01-01",
            fecha_fin="2025-06-01",
            docente_id=1,
            materia_id=1,
            horario="LU",
            aula="103"
        )
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("staff_user:password".encode("utf-8")).decode("utf-8")}'
        }

    # GET
    def test_get_inscripciones_lsit(self):
        url = reverse('inscripciones-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data["results"], [])


    def test_get_inscripciones_by_id (self):
        inscripcion = ComisionAlumnos.objects.create(
            comision=self.comision,
            alumno=self.alumno
        )
        id = inscripcion.id
        url = reverse('inscripciones-detail', kwargs={'pk': id})
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ComisionAlumnos.objects.count(), id)
        self.assertEqual(ComisionAlumnos.objects.get(id=id).alumno, self.alumno)

    # POST

    def test_post_inscripciones(self):
        url = reverse('inscripciones-list')
        response = self.client.post(url, data_inscripcion, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ComisionAlumnos.objects.count(), 1)
        self.assertEqual(ComisionAlumnos.objects.get(id=1).alumno, self.alumno)

    # PUT

    def test_put_inscripciones(self):
        alumno = Alumno.objects.create(
            nombre="Test02",
            apellido="Alumno02",
            email="alumno02@bootcamp.com",
        )
        inscripcion = ComisionAlumnos.objects.create(
            comision=self.comision,
            alumno=self.alumno
        )
        data_inscripcion["alumno"] = alumno.id
        url = reverse('inscripciones-detail', kwargs={'pk': inscripcion.id})
        response = self.client.put(url, data_inscripcion, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ComisionAlumnos.objects.get(id=inscripcion.id).alumno, alumno)

    # DELETE

    def test_delete_inscripciones(self):
        alumno = Alumno.objects.create(
            nombre="Test02",
            apellido="Alumno02",
            email="alumno02@bootcamp.com",
        )
        inscripcion = ComisionAlumnos.objects.create(
            comision=self.comision,
            alumno=alumno
        )
        id = inscripcion.id
        url = reverse('inscripciones-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ComisionAlumnos.objects.filter(id=id).exists())

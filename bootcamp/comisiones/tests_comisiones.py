from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from comisiones.models import Comision
from personas.models import Coordinador, Docente, Alumno
from materias.models import Materia
from especialidad.models import Especialidad
from materias.models import Materia
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64
import pdb


data_comision = {
	"nombre": "Django Intermedio",
    "fecha_inicio": "2025-01-01",
    "fecha_fin": "2025-06-01",
    "docente": 1,
    "materia": 1,
    "horario": "LU",
    "aula": "103"
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
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("staff_user:password".encode("utf-8")).decode("utf-8")}'
        }

    # GET
    def test_get_comisiones_lsit(self):
        url = reverse('comisiones-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data["results"], [])


    def test_get_comisiones_by_id (self):
        comision = Comision.objects.create(
            nombre="Django Intermedio",
            fecha_inicio="2025-01-01",
            fecha_fin="2025-06-01",
            docente_id=1,
            materia_id=1,
            horario="LU",
            aula="103"
        )
        id = comision.id
        url = reverse('comisiones-detail', kwargs={'pk': id})
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comision.objects.count(), 1)
        self.assertEqual(Comision.objects.get(id=1).nombre, 'Django Intermedio')

    # POST

    def test_post_comisiones(self):
        url = reverse('comisiones-list')
        response = self.client.post(url, data_comision, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comision.objects.count(), 1)
        self.assertEqual(Comision.objects.get(id=1).nombre, 'Django Intermedio')

    # PUT

    def test_put_comisiones(self):
        data_comision["nombre"] = "Test de Put"
        comision = Comision.objects.create(
            nombre="Django Intermedio",
            fecha_inicio="2025-01-01",
            fecha_fin="2025-06-01",
            docente_id=1,
            materia_id=1,
            horario="LU",
            aula="103"
        )
        id = comision.id
        url = reverse('comisiones-detail', kwargs={'pk': id})
        response = self.client.put(url, data_comision, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comision.objects.get(id=id).nombre, 'Test de Put')

    # DELETE


    def test_delete_comisiones(self):
        comision = Comision.objects.create(
            nombre="Django Intermedio",
            fecha_inicio="2025-01-01",
            fecha_fin="2025-06-01",
            docente_id=1,
            materia_id=1,
            horario="LU",
            aula="103"
        )
        id = comision.id
        url = reverse('comisiones-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comision.objects.filter(id=id).exists())


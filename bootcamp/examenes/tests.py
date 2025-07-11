from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from comisiones.models import Comision
from personas.models import Docente
from materias.models import Materia
from especialidad.models import Especialidad
from examenes.models import Examen
from comisiones.models import Comision
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64
import datetime
import pdb


data_examen = {
    "comision": 1,
    "fecha": "2025-07-01",
    "hora_inicio": "9:00",
    "hora_fin": "10:00"
}

class MateriasViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
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
    def test_get_examenes_lsit(self):
        url = reverse('examenes-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data["results"], [])

    def test_get_examenes_by_id (self):
        examen = Examen.objects.create(
            comision_id=1,
            fecha="2025-07-01",
            hora_inicio="9:00",
            hora_fin="10:00")
        id = examen.id
        url = reverse('examenes-detail', kwargs={'pk': id})
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Examen.objects.count(), 1)
        self.assertEqual(Examen.objects.get(id=1).comision, self.comision)

    # POST

    def test_post_examenes(self):
        url = reverse('examenes-list')
        response = self.client.post(url, data_examen, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Examen.objects.count(), 1)
        self.assertEqual(Examen.objects.get(id=1).comision, self.comision)

    # PUT

    def test_put_examenes(self):
        data_examen["hora_fin"] = "11:00"
        examen = Examen.objects.create(
            comision_id=1,
            fecha="2025-07-01",
            hora_inicio="9:00",
            hora_fin="10:00")
        id = examen.id
        url = reverse('examenes-detail', kwargs={'pk': id})
        response = self.client.put(url, data_examen, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Examen.objects.get(id=id).hora_fin, datetime.time(11, 0))

    # DELETE


    def test_delete_examenes(self):
        examen = Examen.objects.create(
            comision_id=1,
            fecha="2025-07-01",
            hora_inicio="9:00",
            hora_fin="10:00")
        id = examen.id
        url = reverse('examenes-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Examen.objects.filter(id=id).exists())


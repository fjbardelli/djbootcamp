from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from personas.models import Coordinador, Docente, Alumno
from especialidad.models import Especialidad
from materias.models import Materia
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64
import pdb


data_materia = {
    "nombre": "Historia",
    "codigo": "HIS01",
    "especialidad": 1,
    "creditos": "100",
    "descripcion": "Roma",
    "activa": False
}

class MateriasViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test_user', 'testuser@example.com', 'password')
        self.staff = User.objects.create_user('staff_user', 'staff@example.com', 'password'
                                            , is_staff=True)
        self.especialidad = Especialidad.objects.create(nombre="Especialidad Test",
                                                        descripcion="Descripción Test")
        self.coordinador = Coordinador.objects.create(
            nombre="Test",
            apellido="Coordinador",
            email="coordinador@bootcamp.com",
        )
        self.docente = Docente.objects.create(
            nombre="Test",
            apellido="Docente",
            email="docente@bootcamp.com",
            especialidad_id=self.especialidad.id
        )
        self.alumno = Alumno.objects.create(
            nombre="Test",
            apellido="Alumno",
            email="alumno@bootcamp.com",
        )
        self.headers_staff = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("staff_user:password".encode("utf-8")).decode("utf-8")}'
        }
        self.headers = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("test_user:password".encode("utf-8")).decode("utf-8")}'
        }

        self.headers_not_user = {
            'Content-Type': 'application/json',
        }
        self.headers_coordinador = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("testcoordinador:password_123".encode("utf-8")).decode("utf-8")}'
        }
        self.headers_docente = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("testdocente:password_123".encode("utf-8")).decode("utf-8")}'
        }
        self.headers_alumno = {
            'Content-Type': 'application/json',
            'HTTP_AUTHORIZATION': f'Basic {base64.b64encode("testalumno:password_123".encode("utf-8")).decode("utf-8")}'
        }

    # GET
    def test_get_materias_authenticated_user(self):
        url = reverse('materias-list')
        response = self.client.get(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_materias_user_not_staff (self):
        url = reverse('materias-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_materias_not_ser(self):
        url = reverse('materias-list')
        response = self.client.get(url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST

    def test_post_materias_without_authentication(self):
        url = reverse('materias-list')
        response = self.client.post(url, data_materia, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_materias_with_no_staff(self):
        url = reverse('materias-list')
        response = self.client.post(url, data_materia, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_materias_with_staff(self):
        url = reverse('materias-list')
        response = self.client.post(url, data_materia, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Materia.objects.count(), 1)
        self.assertEqual(Materia.objects.get(id=1).nombre, 'Historia')

    def test_post_materias_with_coordinador(self):
        url = reverse('materias-list')
        response = self.client.post(url, data_materia, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Materia.objects.count(), 1)
        self.assertEqual(Materia.objects.get(id=1).nombre, 'Historia')

    def test_post_materias_with_alumno(self):
        url = reverse('materias-list')
        response = self.client.post(url, data_materia, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # PUT

    def test_put_materias_without_authentication(self):
        data_materia["especialidad"] = self.especialidad
        materia = Materia.objects.create(**data_materia)
        id = materia.id
        data_materia["descripcion"] = "test"
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.put(url, data_materia, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_materias_with_no_staff(self):
        data_materia["especialidad"] = self.especialidad
        materia = Materia.objects.create(**data_materia)
        id = materia.id
        data_materia["descripcion"] = "test"
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.put(url, data_materia, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_materias_with_alumno(self):
        data_materia["especialidad"] = self.especialidad
        materia = Materia.objects.create(**data_materia)
        id = materia.id
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.put(url, data_materia, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # DELETE

    def test_delete_materias_without_authentication(self):
        data_materia["especialidad"] = self.especialidad
        materia = Materia.objects.create(**data_materia)
        id = materia.id
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_materias_with_no_staff(self):
        data_materia["especialidad"] = self.especialidad
        materia = Materia.objects.create(**data_materia)
        id = materia.id
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_materias_with_staff(self):
        data_materia["especialidad"] = self.especialidad
        especilidad = Materia.objects.create(**data_materia)
        id = especilidad.id
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Materia.objects.filter(id=id).exists())

    def test_delete_materias_with_coordinador(self):
        data_materia["especialidad"] = self.especialidad
        especilidad = Materia.objects.create(**data_materia)
        id = especilidad.id
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Materia.objects.filter(id=id).exists())

    def test_delete_materias_with_alumno(self):
        data_materia["especialidad"] = self.especialidad
        materia = Materia.objects.create(**data_materia)
        id = materia.id
        url = reverse('materias-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
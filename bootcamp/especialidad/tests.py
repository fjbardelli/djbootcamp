from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from personas.models import Coordinador, Docente, Alumno
from especialidad.models import Especialidad
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64


data_especialidad = {
    "nombre": "Matemática",
	"descripcion": "Clase de Matemática",
    "activo": True
}

class EspecialidadesViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test_user', 'testuser@example.com', 'password')
        self.staff = User.objects.create_user('staff_user', 'staff@example.com', 'password'                                           
                                            , is_staff=True)
        self.especialidad = Especialidad.objects.create(nombre="Especialidad Test", descripcion="Descripción Test")

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
    def test_get_especialidades_authenticated_user(self):
        url = reverse('especialidad-list')
        response = self.client.get(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_especialidades_user_not_staff (self):
        url = reverse('especialidad-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_especialidades_not_ser(self):
        url = reverse('especialidad-list')
        response = self.client.get(url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST

    def test_post_especialidades_without_authentication(self):
        url = reverse('especialidad-list')
        response = self.client.post(url, data_especialidad, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_especialidades_with_no_staff(self):

        url = reverse('especialidad-list')
        response = self.client.post(url, data_especialidad, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_especialidades_with_staff(self):

        url = reverse('especialidad-list')
        response = self.client.post(url, data_especialidad, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Especialidad.objects.count(), 2)
        self.assertEqual(Especialidad.objects.get(id=2).nombre, 'Matemática')

    def test_post_especialidades_with_coordinador(self):
        url = reverse('especialidad-list')
        response = self.client.post(url, data_especialidad, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Especialidad.objects.count(), 2)
        self.assertEqual(Especialidad.objects.get(id=2).nombre, 'Matemática')

    def test_post_especialidades_with_alumno(self):
        url = reverse('especialidad-list')
        response = self.client.post(url, data_especialidad, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # PUT

    def test_put_especialidades_without_authentication(self):
        especialidad = Especialidad.objects.create(**data_especialidad)
        id = especialidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.put(url, data_especialidad, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_especialidades_with_no_staff(self):
        especiliada = Especialidad.objects.create(**data_especialidad)
        id = especiliada.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.put(url, data_especialidad, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_especialidades_with_staff(self):

        especialidad = Especialidad.objects.create(**data_especialidad)
        id = especialidad.id
        data_especialidad["descripcion"] = "test"
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.put(url, data_especialidad, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Especialidad.objects.get(id=id).descripcion, 'test')


    def test_put_especialidades_with_coordinador(self):

        especialidad = Especialidad.objects.create(**data_especialidad)
        id = especialidad.id
        data_especialidad["descripcion"] = "test"
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.put(url, data_especialidad, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Especialidad.objects.get(id=id).descripcion, 'test')

    def test_put_especialidades_with_alumno(self):
        especialidad = Especialidad.objects.create(**data_especialidad)
        id = especialidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.put(url, data_especialidad, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # DELETE

    def test_delete_especialidades_without_authentication(self):
        especilidad = Especialidad.objects.create(**data_especialidad)
        id = especilidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_especialidades_with_no_staff(self):
        especialidad = Especialidad.objects.create(**data_especialidad)
        id = especialidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_especialidades_with_staff(self):
        especilidad = Especialidad.objects.create(**data_especialidad)
        id = especilidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Especialidad.objects.filter(id=id).exists())

    def test_delete_especialidades_with_coordinador(self):
        especilidad = Especialidad.objects.create(**data_especialidad)
        id = especilidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Especialidad.objects.filter(id=id).exists())

    def test_delete_especialidades_with_alumno(self):
        especialidad = Especialidad.objects.create(**data_especialidad)
        id = especialidad.id
        url = reverse('especialidad-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_alumno)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
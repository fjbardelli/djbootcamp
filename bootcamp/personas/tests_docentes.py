from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Docente, Coordinador
from especialidad.models import Especialidad
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64

data_docente = {
    "nombre": "Docente",
    "apellido": "01",
    "email": "doc_01@bootcamp.com",
    "especialidad_id": 1
}

class docentesViewSetTest(APITestCase):

    def setUp(self):
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
        self.client = APIClient()
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


    # GET
    def test_get_docentes_authenticated_user(self):
        url = reverse('docentes-list')
        response = self.client.get(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_docentes_user_not_staff (self):
        url = reverse('docentes-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_docentes_not_ser(self):
        url = reverse('docentes-list')
        response = self.client.get(url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST

    def test_post_Docente_without_authentication(self):

        url = reverse('docentes-list')
        response = self.client.post(url, data_docente, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_Docente_with_no_staff(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('docentes-list')
        response = self.client.post(url, data_docente, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_Docente_with_staff(self):
        url = reverse('docentes-list')
        response = self.client.post(url, data_docente, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Docente.objects.count(), 2)
        self.assertEqual(Docente.objects.get(id=1).nombre, 'Test')

    def test_post_Docente_with_coordinador(self):
        url = reverse('docentes-list')
        response = self.client.post(url, data_docente, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Docente.objects.count(), 2)
        self.assertEqual(Docente.objects.get(id=1).nombre, 'Test')

    def test_post_Docente_with_docente(self):
        url = reverse('docentes-list')
        response = self.client.post(url, data_docente, **self.headers_docente)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # PUT

    def test_put_Docente_without_authentication(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.put(url, data_docente, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_Docente_without_authentication(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.put(url, data_docente, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_Docente_with_no_staff(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.put(url, data_docente, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_Docente_with_staff(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        data_docente["telefono"] = "5491155558888"
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.put(url, data_docente, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Docente.objects.get(id=id).telefono, '5491155558888')

    def test_put_Docente_with_coordinador(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        data_docente["telefono"] = "5491155558888"
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.put(url, data_docente, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Docente.objects.get(id=id).telefono, '5491155558888')
    # DELETE

    def test_delete_Docente_without_authentication(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_Docente_with_no_staff(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_Docente_with_staff(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Docente.objects.filter(id=id).exists())

    def test_delete_Docente_with_coordinador(self):
        docente = Docente.objects.create(**data_docente)
        id = docente.id
        url = reverse('docentes-detail', kwargs={'pk': id})
        response = self.client.delete(url, **self.headers_coordinador)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Docente.objects.filter(id=id).exists())
from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Coordinador
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import base64


data_coordinador = {
    "nombre": "Coordinador",
    "apellido": "06",
    "email": "coo_06@bootcamp.com",
    "telefono": "5491144447774"
}

class CoordinadoresViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('test_user', 'testuser@example.com', 'password')
        self.staff = User.objects.create_user('staff_user', 'staff@example.com', 'password'
                                            , is_staff=True)
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
    # GET
    def test_get_coordinadores_authenticated_user(self):
        url = reverse('coordinadores-list')
        response = self.client.get(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_coordinadores_user_not_staff (self):
        url = reverse('coordinadores-list')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_coordinadores_not_ser(self):
        url = reverse('coordinadores-list')
        response = self.client.get(url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST

    def test_post_coordinador_without_authentication(self):
        url = reverse('coordinadores-list')
        response = self.client.post(url, data_coordinador, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_coordinador_with_no_staff(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('coordinadores-list')
        response = self.client.post(url, data_coordinador, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_coordinador_with_staff(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('coordinadores-list')
        response = self.client.post(url, data_coordinador, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Coordinador.objects.count(), 1)
        self.assertEqual(Coordinador.objects.get(id=1).nombre, 'Coordinador')

    # PUT

    def test_put_coordinador_without_authentication(self):
        coordinador = Coordinador.objects.create(**data_coordinador)
        id = coordinador.id
        url = reverse('coordinadores-detail', kwargs={'pk': id})
        response = self.client.put(url, data_coordinador, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_coordinador_with_no_staff(self):
        coordinador = Coordinador.objects.create(**data_coordinador)
        id = coordinador.id
        url = reverse('coordinadores-detail', kwargs={'pk': id})
        response = self.client.put(url, data_coordinador, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_coordinador_with_staff(self):

        coordinador = Coordinador.objects.create(**data_coordinador)
        id = coordinador.id
        data_coordinador["telefono"] = "5491155558888"
        url = reverse('coordinadores-detail', kwargs={'pk': id})
        response = self.client.put(url, data_coordinador, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Coordinador.objects.get(id=id).telefono, '5491155558888')

    # DELETE

    def test_delete_coordinador_without_authentication(self):
        coordinador = Coordinador.objects.create(**data_coordinador)
        id = coordinador.id
        url = reverse('coordinadores-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_coordinador_with_no_staff(self):
        coordinador = Coordinador.objects.create(**data_coordinador)
        id = coordinador.id
        url = reverse('coordinadores-detail', kwargs={'pk': id})
        response = self.client.delete(path=url, **self.headers_not_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_coordinador_with_staff(self):
        coordinador = Coordinador.objects.create(**data_coordinador)
        id = coordinador.id
        url = reverse('coordinadores-detail', kwargs={'pk': id})
        #response = self.client.delete(url, HTTP_AUTHORIZATION=self.headers_staff['HTTP_AUTHORIZATION'], HTTP_CONTENT_TYPE=self.headers_staff['Content-Type'])
        response = self.client.delete(url, **self.headers_staff)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Coordinador.objects.filter(id=id).exists())

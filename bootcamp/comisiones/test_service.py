from django.test import TestCase
from comisiones.models import Comision
from personas.models import Docente
from materias.models import Materia
from especialidad.models import Especialidad
from comisiones.services import ComisionService, ComisionEmailService, ComisionError
import pdb

class TestComisionesService(TestCase):
    def setUp(self):
        self.especialidad = Especialidad.objects.create(nombre="Especialidad Test", descripcion="Descripción Test")
        self.docente = Docente.objects.create(
            nombre="Test",
            apellido="Docente",
            email="docente@bootcamp.com",
            especialidad=self.especialidad)
        self.materia = Materia.objects.create(
            nombre="Historia",
            codigo="HIS01",
            especialidad=self.especialidad
        )
        self.service = ComisionService(mail_service=ComisionEmailService)
    def test_create_comision(self):
        comision = self.service.crear_comision(
            materia=self.materia.id,
            docente=self.docente.id,
            nombre="Historia de Roma",
            inicio="2025-01-01",
            fin="2025-06-01",
            horario="LU",
            aula="101"
        )
        self.assertIsInstance(comision, Comision)
        self.assertEqual(comision.nombre, "Historia de Roma")
        self.assertEqual(comision.docente, self.docente)
        self.assertEqual(comision.materia, self.materia)

    def test_comision_docente_inactivo(self):
        docente = Docente.objects.create(
            nombre="Test",
            apellido="Inactivo",
            email="docente_ina@bootcamp.com",
            especialidad=self.especialidad,
            activo=False)

        with self.assertRaises(ComisionError):
            comision = self.service.crear_comision(
                materia=self.materia.id,
                docente=docente.id,
                nombre="Historia de Roma",
                inicio="2025-01-01",
                fin="2025-06-01",
                horario="LU",
                aula="101"
            )

    def test_comision_materia_inactiva(self):
        materia = Materia.objects.create(
            nombre="Matemáticas",
            codigo="HIS02",
            especialidad=self.especialidad,
            activa=False
        )

        with self.assertRaises(ComisionError):
            comision = self.service.crear_comision(
                materia=materia.id,
                docente=self.docente.id,
                nombre="Historia de Roma",
                inicio="2025-01-01",
                fin="2025-06-01",
                horario="LU",
                aula="101"
            )

    def test_comision_distinta_especialidad(self):
        materia = Materia.objects.create(
            nombre="Matemáticas",
            codigo="HIS02",
            especialidad=self.especialidad,
            activa=False
        )

        with self.assertRaises(ComisionError):
            comision = self.service.crear_comision(
                materia=materia.id,
                docente=self.docente.id,
                nombre="Historia",
                inicio="2025-01-01",
                fin="2025-06-01",
                horario="LU",
                aula="101"
            )

    def test_comision_docente_ocupado(self):
        especialidad = Especialidad.objects.create(nombre="Especialidad 2", descripcion="Descripción 2")
        materia = Materia.objects.create(
            nombre="Matemáticas",
            codigo="HIS02",
            especialidad=especialidad,
            activa=False
        )

        with self.assertRaises(ComisionError):
            comision = self.service.crear_comision(
                materia=materia.id,
                docente=self.docente.id,
                nombre="Historia de Roma",
                inicio="2025-01-01",
                fin="2025-06-01",
                horario="LU",
                aula="101"
            )

    def test_comision_aula_ocupada(self):
        especialidad = Especialidad.objects.create(nombre="Especialidad 2", descripcion="Descripción 2")
        materia = Materia.objects.create(
            nombre="Matemáticas",
            codigo="HIS02",
            especialidad=especialidad,
            activa=False
        )
        docente = Docente.objects.create(
            nombre="Test01",
            apellido="Docente01",
            email="docente01@bootcamp.com",
            especialidad=self.especialidad)
        with self.assertRaises(ComisionError):
            comision = self.service.crear_comision(
                materia=materia.id,
                docente=docente.id,
                nombre="Aula Ocupada",
                inicio="2025-01-01",
                fin="2025-06-01",
                horario="LU",
                aula="101"
            )
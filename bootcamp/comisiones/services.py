from django.shortcuts import get_object_or_404
from datetime import date
from django.utils import timezone
from django.db import transaction

from comisiones.models import Comision
from comisiones.errors import ComisionError
from personas.models import Docente
from materias.models import Materia
import pdb


class ComisionEmailService:
    def send_confirmation_mail(self):
        print("<<< Comisión confirmada al docente >>>")


class ComisionService:
    def __init__(
            self,
            mail_service: ComisionEmailService,
        ) -> None:
        self.mail_service = mail_service()

    @transaction.atomic
    def crear_comision(
        self,
        *,
        materia: Materia,
        docente: Docente,
        nombre: str,
        inicio: date,
        fin: date,
        horario: str,
        aula: str):

        docente:Docente = get_object_or_404(Docente, id=docente)
        materia:Materia = get_object_or_404(Materia, id=materia)

        if not docente or docente.activo == False:
            raise ComisionError('Docente requerido o no esta activo')
        if not materia or not materia.activa:
            raise ComisionError('Esta materia no puede ser asignada')
        if docente.especialidad != materia.especialidad:
            raise ComisionError('El docente no esta habilitado para dar esta materia')
        if  not fin > inicio:
            raise ComisionError('La fecha de inicio no puede ser posterior a la fecha de fin')
        if  Comision.objects.filter(
            aula=aula,
            horario=horario,
        ).exists():
            raise ComisionError('Ya existe una comisión con el mismo aula y horario')
        if  Comision.objects.filter(
            docente=docente,
            horario=horario,
        ).exists():
            raise ComisionError('El docente ya tiene una comisión asignada en este horario')

        try:
            comision = Comision.objects.create(
                materia=materia,
                docente=docente,
                nombre=nombre,
                fecha_inicio=inicio,
                fecha_fin=fin,
                horario=horario,
                aula=aula
            )
            self.mail_service.send_confirmation_mail()
            return comision
        except Exception as e:
            raise ComisionError('No fue posible completar la operación') from e
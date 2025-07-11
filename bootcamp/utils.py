# utils/responses.py

from rest_framework.response import Response
from rest_framework import status

class DRFResponse:

    @staticmethod
    def success(data=None, message="Operación exitosa.", status_code=status.HTTP_200_OK):
        return Response({
            "success": True,
            "message": message,
            "data": data,
            "errors": None
        }, status=status_code)

    @staticmethod
    def created(data=None, message="Recurso creado exitosamente."):
        return DRFResponse.success(data, message, status.HTTP_201_CREATED)

    @staticmethod
    def error(message="Ocurrió un error.", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "success": False,
            "message": message,
            "data": None,
            "errors": errors
        }, status=status_code)

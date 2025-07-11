# Utilizar la imagen oficial de Python 3.9
FROM python:3.12.11-alpine3.21

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app
COPY ./bootcamp /app

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto 8000
EXPOSE 8000

# Definir el comando para ejecutar la app
CMD ["gunicorn", "bootcamp.wsgi:application", "--workers", "3", "--bind", "0.0.0.0:8000"]
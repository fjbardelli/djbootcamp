FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bootcamp .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "bootcamp.wsgi:application", "--workers=3", "--bind=0.0.0.0:8000"]

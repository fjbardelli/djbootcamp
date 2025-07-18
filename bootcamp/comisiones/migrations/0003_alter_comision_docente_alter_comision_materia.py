# Generated by Django 5.2.4 on 2025-07-13 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comisiones', '0002_comisionalumnos'),
        ('materias', '0001_initial'),
        ('personas', '0004_alter_alumno_options_alter_docente_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comision',
            name='docente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='com_docente', to='personas.docente'),
        ),
        migrations.AlterField(
            model_name='comision',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='com_materia', to='materias.materia'),
        ),
    ]

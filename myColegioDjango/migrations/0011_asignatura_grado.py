# Generated by Django 5.1.5 on 2025-04-08 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myColegioDjango', '0010_alter_grado_nombre_asignatura'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignatura',
            name='grado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asignaturas', to='myColegioDjango.grado'),
        ),
    ]

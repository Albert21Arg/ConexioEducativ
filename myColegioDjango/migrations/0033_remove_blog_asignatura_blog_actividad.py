# Generated by Django 5.2 on 2025-05-21 22:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myColegioDjango', '0032_actividad_asignatura'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='asignatura',
        ),
        migrations.AddField(
            model_name='blog',
            name='actividad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blogs', to='myColegioDjango.actividad'),
        ),
    ]

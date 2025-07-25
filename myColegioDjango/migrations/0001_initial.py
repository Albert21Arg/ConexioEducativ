# Generated by Django 5.1.5 on 2025-04-05 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('nick', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=254)),
                ('rol', models.CharField(choices=[('ADM', 'Administrador'), ('COR', 'Coordinador Académico'), ('SEC', 'Secretari@'), ('VIS', 'Visitante')], max_length=3)),
                ('correo', models.CharField(max_length=254, unique=True)),
                ('foto', models.ImageField(upload_to='fotos')),
                ('token_recuperar_clave', models.CharField(default='', max_length=6)),
            ],
        ),
    ]

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Solo permitir texto
sololetras = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
    message='Este campo solo puede contener letras y espacios.'
)

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100, validators=[sololetras])
    apellido = models.CharField(max_length=100, validators=[sololetras])
    apellido = models.CharField(max_length=100)
    password = models.CharField(max_length=254)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    ROLES = (
        ("ADM", "Administrador"),
        ("PROF", "Profesor"),
        ("EST", "Estudiante"),

    )
    rol = models.CharField(max_length=4, choices=ROLES)
    correo =  models.EmailField(max_length=254, unique=True)
    foto = models.ImageField(upload_to="fotos", blank=True, null=True)
    token_recuperar_clave = models.CharField(max_length=6, default="")

    def __str__(self):
        return f"{self.nombre} {self.apellido})"

class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'


class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    grado = models.ForeignKey('Grados', on_delete=models.SET_NULL, null=True, blank=True, related_name="estudiantes")
    
    def __str__(self):
        return f'{self.usuario.nombre} {self.usuario.apellido}'

class Grados(models.Model):
    
    nombre = models.CharField(max_length=20, unique=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name="grados")
    estudiante = models.ManyToManyField(Estudiante, blank=True, related_name="grados")
    descripcion = models.TextField(blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.nombre 
    
    @property
    def fechaSoloFecha(self):
        return self.fechaCreacion.date()

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, unique=False)
    descripcion = models.TextField(blank=True, null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name="asignaturas")
    grados = models.ForeignKey(Grados, on_delete=models.SET_NULL, null=True, blank=True, related_name="asignaturas")
    
    
    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True, blank=True, related_name="actividades")

    def __str__(self):
        return self.nombre
    

class Blog(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    actividad = models.ForeignKey(Actividad, on_delete=models.SET_NULL, null=True, blank=True, related_name="blogs")
    grados = models.ForeignKey(Grados, on_delete=models.SET_NULL, null=True, blank=True, related_name="blogs")
    def __str__(self):
        return self.titulo
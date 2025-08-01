from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id','nombre', 'apellido', 'rol', 'correo', 'foto']
    
@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_nombre', 'get_apellido', 'get_rol', 'get_correo', 'get_foto']

    def get_nombre(self, obj):
        return obj.usuario.nombre
    get_nombre.short_description = 'Nombre'

    def get_apellido(self, obj):
        return obj.usuario.apellido
    get_apellido.short_description = 'Apellido'

    
    def get_rol(self, obj):
        return obj.usuario.get_rol_display()
    get_rol.short_description = 'Rol'

    def get_correo(self, obj):
        return obj.usuario.correo
    get_correo.short_description = 'Correo'

    def get_foto(self, obj):
        return obj.usuario.foto.url if obj.usuario.foto else ''
    get_foto.short_description = 'Foto'
    
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_nombre', 'get_apellido', 'get_rol', 'get_correo', 'get_foto']

    def get_nombre(self, obj):
        return obj.usuario.nombre
    get_nombre.short_description = 'Nombre'

    def get_apellido(self, obj):
        return obj.usuario.apellido
    get_apellido.short_description = 'Apellido'

    def get_rol(self, obj):
        return obj.usuario.get_rol_display()
    get_rol.short_description = 'Rol'

    def get_correo(self, obj):
        return obj.usuario.correo
    get_correo.short_description = 'Correo'

    def get_foto(self, obj):
        return obj.usuario.foto.url if obj.usuario.foto else ''
    get_foto.short_description = 'Foto'

@admin.register(Grados)
class GradosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'listar_estudiantes', 'fechaCreacion')

    def listar_estudiantes(self, obj):
        return ", ".join([str(est) for est in obj.estudiante.all()])
    listar_estudiantes.short_description = 'Estudiantes'

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('id' ,'nombre', 'fechaCreacion')
    search_fields = ('nombre',)
    
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('id' ,'nombre', 'descripcion', 'fecha_limite')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_limite',)
    
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id' ,'titulo', 'contenido', 'fechaCreacion')
    search_fields = ('titulo', 'contenido')
    list_filter = ('fechaCreacion',)
    
@admin.register(Nota)
class NotaActividadAdmin(admin.ModelAdmin):
    list_display = ('id', 'estudiante_nombre', 'actividad_nombre', 'valor', 'porcentaje')

    def estudiante_nombre(self, obj):
        return f"{obj.estudiante.usuario.nombre} {obj.estudiante.usuario.apellido}"
    estudiante_nombre.short_description = "Estudiante"

    def actividad_nombre(self, obj):
        return obj.actividad.nombre
    actividad_nombre.short_description = "Actividad"
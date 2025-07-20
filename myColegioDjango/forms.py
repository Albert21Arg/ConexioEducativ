from django import forms
from .models import *
from django.core.exceptions import ValidationError

# Formulario para Login
class LoginForm(forms.Form):
    correo = forms.CharField(label="Usuario", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# Formulario para cambio de contraseña
class CambioPasswordForm(forms.Form):
    vieja = forms.CharField(widget=forms.PasswordInput, label="Contraseña actual")
    nueva = forms.CharField(widget=forms.PasswordInput, label="Nueva contraseña")
    nueva_repiti = forms.CharField(widget=forms.PasswordInput, label="Repetir nueva contraseña")

# Formulario para recuperación de contraseña (ingresar correo)
class RecuperarPasswordForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico")

# Formulario para verificar token y nueva contraseña
class VerificarTokenForm(forms.Form):
    correo = forms.EmailField(widget=forms.HiddenInput())
    token = forms.CharField(label="Token de seguridad")
    password = forms.CharField(widget=forms.PasswordInput, label="Nueva contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo',  'rol', 'foto']
        

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto']

class UsuarioSListarForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        label="Seleccione un usuario",
        empty_label="(Seleccione)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
class GradosForm(forms.ModelForm):
    class Meta:
        model = Grados
        fields = ['nombre', 'descripcion','profesor','estudiante']
        
class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'descripcion','profesor','grados']
        
class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'fecha_limite']
        widgets = {
            'fecha_limite': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            })
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'contenido','actividad','grados']
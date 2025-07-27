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
    
from django import forms
from django.db import models
from .models import Grados, Estudiante

class GradosForm(forms.ModelForm):
    estudiantes = forms.ModelMultipleChoiceField(
        queryset=Estudiante.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Estudiantes sin grupo"
    )

    class Meta:
        model = Grados
        fields = ['nombre', 'descripcion', 'profesor']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del grado'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese una breve descripción del grado'
            }),
            'profesor': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            # Editar grado existente: permitir estudiantes sin grupo o ya en este grado
            self.fields['estudiantes'].queryset = Estudiante.objects.filter(
                models.Q(grado__isnull=True) | models.Q(grado=self.instance)
            )
            self.fields['estudiantes'].initial = self.instance.estudiantes.all()
        else:
            # Crear nuevo grado: solo estudiantes sin grupo
            self.fields['estudiantes'].queryset = Estudiante.objects.filter(grado__isnull=True)

    def save(self, commit=True):
        instancia = super().save(commit=False)
        if commit:
            instancia.save()
            # Desvincular estudiantes actuales
            Estudiante.objects.filter(grado=instancia).update(grado=None)
            # Asociar nuevos estudiantes
            self.cleaned_data['estudiantes'].update(grado=instancia)
        return instancia

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'descripcion','profesor','grados']
        
from django import forms
from .models import Actividad

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'fecha_limite']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la actividad'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción breve de la actividad'
            }),
            'fecha_limite': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'id': 'id_fecha_limite',
                'placeholder': 'Seleccione fecha y hora límite',
                'type': 'datetime-local'
            }),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'contenido','actividad','grados']
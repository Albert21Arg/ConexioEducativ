# Conexion Educativa

Este es un sistema web hecho con Django pensado para ayudar a gestionar todo lo relacionado con una institución educativa. La idea es tener todo en un solo lugar: desde los grados y materias hasta los estudiantes, profesores, actividades y publicaciones.

El sistema permite crear usuarios con diferentes roles (como estudiante o profesor), y dependiendo del rol que se le asigne, el sistema se encarga de organizarlo automáticamente en su lugar. Por ejemplo, si se registra un profesor, se crea su perfil con la información correspondiente sin tener que hacerlo a mano. Lo mismo pasa con los estudiantes.Todo está pensado para que sea fácil de usar y mantener, tanto para administradores como para los usuarios que se conectan al sistema.

También hay una estructura clara para gestionar grados, materias (asignaturas), y relacionarlas con los estudiantes y profesores, haciendo posible llevar un control académico desde la web. Cada parte de la interfaz busca mantener una apariencia coherente para que no parezca que estás cambiando de aplicación al navegar entre secciones.


## Características principales

- Autenticación de usuarios.
- Gestión de roles (estudiante, profesor, administrador).
- Registro automático en tablas correspondientes al asignar rol.
- Solicitud de datos complementarios en el primer inicio de sesión.
- Asociación de asignaturas con profesores y estudiantes.
- CRUD para grados, asignaturas, actividades y publicaciones.
- Interfaz unificada con diseño consistente.
- Perfil editable del usuario.

##  Tecnologías utilizadas

- [Django](https://www.djangoproject.com/) (Back-end)
- HTML + CSS + Bootstrap (Front-end básico)
- SQLite3 (por defecto)

## 📦 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Albert21Arg/ConexioEducativa.git
   
   python -m venv env

   pip install -r requirements.txt

   python manage.py migrate
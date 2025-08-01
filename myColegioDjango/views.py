# Create your models here.
from django.shortcuts import render, redirect, get_object_or_404
from .utils import *
from .models import *
from .forms import *
from django.core.validators import validate_email
from django.db import IntegrityError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http.response import JsonResponse
import re
from django.db import transaction
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

def login(request):
    if request.method == "POST":
        user = request.POST.get("correo")
        passwd = request.POST.get("password")
        try:
            q = Usuario.objects.get(correo = user)
            if verify_password(passwd, q.password):
                messages.success(request, "Bienvenido!")
                # creación de la sesión...
                request.session["logueado"] = {
                    "id" : q.id,
                    "rol": q.rol,
                    "nombre_rol": q.get_rol_display(),
                    "nombre": f"{q.nombre} {q.apellido}"
                }
                return redirect("index")
            else:
                raise Exception()
        except Usuario.DoesNotExist:
            messages.warning(request, "Usuario o contraseña no válidos")
            request.session["logueado"] = None
        except Exception as e:
            messages.error(request, f"Error: {e}")
            request.session["logueado"] = None
        return redirect("login")
    else:
        verificar = request.session.get("logueado", False)
        if verificar:
            return redirect("index")
        else:
            return render(request, "fijos/login.html")

def logout(request):
    try:
        del request.session["logueado"]
        messages.success(request, "Sesión cerrada correctamente!")
        return redirect("index")
    except:
        messages.error(request, "Ocurrió un error, intente de nuevo.")
        return redirect("principal")
    
def principal(request):
    
        return render(request, "fijos/principal.html")
    
def perfilUsuario(request, id):
    if request.session.get("logueado", {}).get("rol") == "ADM":
        usuario = get_object_or_404(Usuario, id=id)
        return render(request, "formularios/usuarioPerfil.html", {"usuario": usuario})
    else:
        messages.warning(request, "No tienes permiso para ver este perfil.")
        return redirect("index")
    
def index(request):
    verificar = request.session.get("logueado", False)
    if verificar:
        return render(request, "fijos/index.html")
    else:
        
        return redirect("principal")
    
def perfil(request):
    verificar = request.session.get("logueado", False)

    if not verificar or "id" not in verificar:
        return redirect("login")  # redirige al login si no hay sesión

    try:
        q = Usuario.objects.get(id=verificar["id"])
        contexto = {"data": q}
        return render(request, "fijos/perfil.html", contexto)
    except Usuario.DoesNotExist:
        return redirect("login")
    
def registrarUsuarios(request):
    if request.session.get("logueado") :
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            correo = request.POST.get("correo")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            rol = "EST"
            foto = ""

            valid = True 

            # Validar email
            try:
                validate_email(correo)
            except ValidationError:
                messages.error(request, "El correo ingresado no es válido.")
                valid = False

            letras_regex = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')

            if not letras_regex.match(nombre):
                messages.error(request, "El nombre solo puede contener letras y espacios.")
                valid = False

            if not letras_regex.match(apellido):
                messages.error(request, "El apellido solo puede contener letras y espacios.")
                valid = False
            
            dominios = correo.split('@')[-1]
            dominiosValidos = ['hotmail.com','gmail.com', 'outlook.com', '.edu.co', 'outlook.es']  

            if dominios not in dominiosValidos:
                messages.error(request, f"Solo se permiten correos de dominios autorizados.{dominiosValidos}")
                valid = False

            if password != password2:
                messages.warning(request, "Las contraseñas no coinciden.")
                valid = False
            elif len(password) < 6:
                messages.warning(request, "La contraseña debe tener al menos 6 caracteres.")
                valid = False

            if not valid:
                return render(request, "fijos/registrarUsuarios.html", {
                    "nombre": nombre,
                    "apellido": apellido,
                    "correo": correo,
        }) 

            try:
                q = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    rol=rol,
                    foto=foto,
                    password=hash_password(password)
                )
                q.save()
                messages.success(request, "Usuario creado correctamente!")

                try:
                    html_message = f'''
                    <strong>{q.nombre}</strong>, acabas de crear una cuenta en nuestra plataforma Conexion Educativa.<br><br>
                    Tus datos registrados son:<br>
                    <strong>Correo:</strong> {q.correo}<br><br>
                    Si deseas iniciar sesión, haz clic en el siguiente enlace:<br>
                    <a href="http://127.0.0.1:8000/"> Conexión Educativa </a><br><br>'''

                    send_mail(
                        'Registro de Usuario',
                        "",
                        settings.EMAIL_HOST_USER,
                        [q.correo],
                        fail_silently=False,
                        html_message=html_message
                    )
                    messages.success(request, "Correo enviado !!")
                except Exception as error:
                    messages.error(request, f"No se pudo enviar el correo: {error}")

                return redirect("login")

            except IntegrityError:
                messages.error(request, f"Error: {correo} El correo ya está en uso.")
                return redirect("registrarUsuarios")
            except Exception as e:
                messages.error(request, f"Error inesperado: {e}")
                return redirect("registrarUsuarios")

        else:
            return render(request, "fijos/registrarUsuarios.html")
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("login")

def modificarUsuario(request, id):
    if request.session.get("logueado", {}).get("rol") == "ADM":
        usuario = get_object_or_404(Usuario, id=id)

        if request.method == "POST":
            form = UsuarioForm(request.POST, request.FILES, instance=usuario)
            password = request.POST.get("password")

            if form.is_valid():
                if password and len(password) < 6:
                    messages.error(request, "La contraseña debe contener mínimo 6 caracteres.")
                    return render(request, "fijos/modificarUsuario.html", {"form": form, "usuario": usuario})

                usuario = form.save(commit=False)

                if password:
                    usuario.password = make_password(password)

                usuario.save()
                messages.success(request, "Usuario modificado correctamente.")
                return redirect('perfil' if request.session["logueado"]["id"] == id else 'usuariosListar')
            else:
                print("Errores del formulario:", form.errors)
                messages.error(request, "Por favor verifica los datos ingresados.")
        else:
            form = UsuarioForm(instance=usuario)

        return render(request, "fijos/modificarUsuario.html", {"form": form, "usuario": usuario})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

    
def cambioPassword(request):
    verificar = request.session.get("logueado", False)
    
    if verificar:
        if request.method == "POST":
            vieja = request.POST.get("vieja")
            nueva = request.POST.get("nueva")
            nueva_r = request.POST.get("nueva_repiti")
            # capturo usuario logueado ------------------------
            usuario = request.session.get("logueado", False)
            q = Usuario.objects.get(pk = usuario["id"])
            if verify_password(vieja, q.password):
                if nueva == nueva_r:
                    # ecriptar contraseña
                    # from .utils import *
                    q.password = hash_password(nueva)
                    q.save()
                    messages.success(request, "Contraseña cambiada con éxito")
                else:
                    messages.info(request, "Las nuevas contraseñas no coinciden...")
            else:
                messages.warning(request, "Contraseña actual no coincide...")

            return redirect("cambioPassword")
        else:
            return render(request, "fijos/cambioPassword.html")
    
def recuperarPassword(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        try:
            q = Usuario.objects.get(correo = correo)
            from random import randint
            token = randint(100000, 999999)
            q.token_recuperar_clave = token
            chorrera = hash_password("chorrera")
            q.save()
            try:
                html_message = f'<strong>{q.nombre}</strong>, Desde Conexion Educativa hemos recibido una solicitud de cambio de contraseña. Por favor accede al siguiente link e ingresa el token de seguridad:<br><br>TOKEN: {token}<br>Ve al siguiente link: <a href="http://127.0.0.1:8000/verificar_token_recuperar_password/?chorrera={chorrera}&email=True&correo={q.correo}">Conexion Educativa</a>'

                send_mail('Registro de Usuario en Educalab', "", settings.EMAIL_HOST_USER,
                          [f'{q.correo}'],
                          fail_silently=False,
                          html_message=html_message
                          )
                messages.success(request, "Correo enviado !!")
                return redirect("recuperarPassword")
            except Exception as error:
                messages.error(request, f"No se pudo enviar el correo: {error}")
        except Usuario.DoesNotExist:
            messages.info(request, "Si el correo está registrado, recibirás un mensaje.")
            return redirect("recuperarPassword")
    else:
        return render(request, "fijos/recuperarPassword.html")
    
def token(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        token = request.POST.get("token")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        q = Usuario.objects.get(correo=correo)
        if q.token_recuperar_clave == token:
            if password == password2:
                q.token_recuperar_clave = ""
                q.password = hash_password(password)
                q.save()
                messages.success(request, "Contraseña recuperada correctamente!")
                return redirect("login")
            else:
                messages.error(request, "Las Contraseñas no coinciden...")
        else:
            messages.error(request, f"Token inválido")

        return redirect("verificar_token_recuperar_password")
    else:
        correo = request.GET.get("correo")
        contexto={
            "correo": correo
        }
        return render(request, "fijos/verificar_token_recuperar_password.html", contexto)

def editarFotoPerfil(request):
    verificar = request.session.get("logueado", False)
    
    if not verificar:
        return redirect('login')
    else:
        usuario_id = verificar.get("id")
        usuario = get_object_or_404(Usuario, id=usuario_id)

        if request.method == "POST":
            form = FotoPerfilForm(request.POST, request.FILES, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('perfil')
        else:
            form = FotoPerfilForm(instance=usuario)

        return render(request, 'fijos/editarFotoPerfil.html', {'form': form})

def usuariosListar(request):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        usuarios = Usuario.objects.all()
        return render(request, 'formularios/usuariosListar.html', {'usuarios': usuarios})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

def usuariosListar1(request):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        usuarios = list(Usuario.objects.values('id','nombre','apellido','rol','correo'))
        data = {'usuarios': usuarios}
        return JsonResponse(data)
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

def usuariosEliminar(request, id):
    if request.session.get("logueado", {}).get("rol") == "ADM":
        usuario = get_object_or_404(Usuario, id=id)
        if request.method == 'POST':
            usuario.delete()
            messages.success(request, "Usuario eliminado correctamente.")
            return redirect('usuariosListar')  # Usa el nombre de la URL, no una plantilla directamente
        else:
            # Mostrar confirmación antes de eliminar
            return render(request, 'fijos/usuariosEliminarConfirmar.html', {'usuario': usuario})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

#Grados
def gradosCrear(request):
    if request.session.get("logueado") or request.session.get("logueado", {}).get("rol") == "ADM" :
        if request.method == 'POST':
            form = GradosForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('gruposCrear')
        else:
            form = GradosForm()
        return render(request, 'formularios/gruposCrear.html', {'form': form})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

def gradosActualizar(request, grupo_id):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        grupo = get_object_or_404(Grados, id=grupo_id)
        if request.method == 'POST':
            form = GradosForm(request.POST, instance=grupo)
            if form.is_valid():
                form.save()
                return redirect('gradosListar')
        else:
            form = GradosForm(instance=grupo)
        return render(request, 'formularios/gruposActualizar.html', {'form': form, 'grupo': grupo})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

def gradosEliminar(request, grupo_id):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        grupo = get_object_or_404(Grados, id=grupo_id)
        if request.method == 'POST':
            grupo.delete()
            return redirect('gradosListar')
        return render(request, 'formularios/gruposEliminar.html', {'grupo': grupo})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")
    
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Grados, Profesor, Usuario

def gradosListar(request):
    sesion = request.session.get("logueado", {})
    rol = sesion.get("rol")
    usuario_id = sesion.get("id")

    if rol == "ADM":
        grupos = Grados.objects.all()
    elif rol == "PROF":
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            profesor = Profesor.objects.get(usuario=usuario)
            grupos = Grados.objects.filter(profesor=profesor)
        except (Usuario.DoesNotExist, Profesor.DoesNotExist):
            grupos = []
            messages.warning(request, "No tienes grupos asignados.")
    else:
        messages.warning(request, "No tienes permiso para ver esta información.")
        return redirect("index")

    return render(request, 'formularios/gruposListar.html', {'grupos': grupos})

def gradosListar1(request):
    sesion = request.session.get("logueado", {})
    rol = sesion.get("rol")
    usuario_id = sesion.get("id")

    if rol in ["ADM", "PROF"]:
        if rol == "ADM":
            grupos = Grados.objects.all()
        elif rol == "PROF":
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                profesor = Profesor.objects.get(usuario=usuario)
                grupos = Grados.objects.filter(profesor=profesor)
            except (Usuario.DoesNotExist, Profesor.DoesNotExist):
                grupos = []

        data = []
        for grupo in grupos:
            profesor_nombre = "Sin asignar"
            if grupo.profesor and grupo.profesor.usuario:
                profesor_nombre = f"{grupo.profesor.usuario.nombre} {grupo.profesor.usuario.apellido}"

            data.append({
                'id': grupo.id,
                'nombre': grupo.nombre,
                'descripcion': grupo.descripcion,
                'profesorNombre': profesor_nombre,
            })

        return JsonResponse({
            'grados': data,
            'usuario': {
                'rol': rol
            }
        })
    else:
        return JsonResponse({'error': 'No autorizado'}, status=403)
#Asignaturas
def asignaturasListar(request):
    if request.session.get("logueado", {}).get("rol") in ["ADM", "PROF", "EST"]:
        asignaturas = Asignatura.objects.all().order_by('-fechaCreacion')
        return render(request, 'formularios/asignaturasListar.html', {'asignaturas': asignaturas})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("principal") 
    
def asignaturasListar1(request):
    rol = request.session.get("logueado", {}).get("rol")
    usuario_id = request.session.get("logueado", {}).get("id")

    if not usuario_id or not rol:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    usuario = Usuario.objects.get(id=usuario_id)

    if rol == "ADM":
        asignaturas_qs = Asignatura.objects.select_related('profesor__usuario', 'grados').all()

    elif rol == "PROF":
        try: 
            profesor = Profesor.objects.get(usuario=usuario)
            asignaturas_qs = Asignatura.objects.filter(profesor=profesor).select_related('profesor__usuario', 'grados')
        except Profesor.DoesNotExist:
            asignaturas_qs = Asignatura.objects.none()

    elif rol == "EST":
        try:
            estudiante = Estudiante.objects.select_related('grado').get(usuario=usuario)
            asignaturas_qs = Asignatura.objects.filter(grados=estudiante.grado).select_related('profesor__usuario', 'grados')
        except Estudiante.DoesNotExist:
            asignaturas_qs = Asignatura.objects.none()

    else:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    data = {
        'usuario': {
            'rol': rol
        },
        'asignaturas': [
            {
                'id': a.id,
                'nombre': a.nombre,
                'descripcion': a.descripcion,
                'profesorNombre': f"{a.profesor.usuario.nombre} {a.profesor.usuario.apellido}" if a.profesor else "",
                'grados': a.grados.nombre if a.grados else ""
            }
            for a in asignaturas_qs
        ]
    }

    return JsonResponse(data)




def asignaturasCrear(request):
    if request.session.get("logueado", {}).get("rol") == "ADM":
        if request.method == 'POST':
            form = AsignaturaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('asignaturasListar')
        else:
            form = AsignaturaForm()
        return render(request, 'formularios/asignaturasCrear.html', {'form': form, 'accion': 'Crear'})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")
    
def asignaturasActualizar(request, id):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        asignatura = get_object_or_404(Asignatura, id=id)
        if request.method == 'POST':
            form = AsignaturaForm(request.POST, instance=asignatura)
            if form.is_valid():
                form.save()
                return redirect('asignaturasListar')
        else:
            form = AsignaturaForm(instance=asignatura)
        return render(request, 'formularios/asignaturasActualizar.html', {'form': form, 'accion': 'Actualizar'})

def asignaturasEliminar(request, id):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        asignatura = get_object_or_404(Asignatura, id=id)
        if request.method == 'POST':
            asignatura.delete()
            return redirect('asignaturasListar')
        return render(request, 'formularios/asignaturasEliminar.html', {'asignatura': asignatura})

#Estudiantes
def estudiantesListar(request):
    if request.session.get("logueado", {}).get("rol") == "ADM" or "PROF" :
        estudiantes = Estudiante.objects.all()
        return render(request, 'formularios/estudiantesListar.html', {'estudiantes': estudiantes})

def usuariosListar2(request):
    if request.session.get("logueado", {}).get("rol") == "ADM" or "PROF" :
        usuarios = list(Usuario.objects.filter(rol="EST").values('nombre','apellido','correo'))
        data = {'usuarios': usuarios}
        return JsonResponse(data)
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

#Actividades
def actividadCrear(request, asignatura_id):
    if request.session.get("logueado", {}).get("rol") in ["ADM", "PROF"]:
        asignatura = get_object_or_404(Asignatura, id=asignatura_id)
        
        if request.method == "POST":
            form = ActividadForm(request.POST)
            if form.is_valid():
                actividad = form.save(commit=False)
                actividad.asignatura = asignatura  # Asignar la relación manualmente
                actividad.save()
                return redirect('asignaturasListar')  # Puedes redirigir a la lista o al detalle
        else:
            form = ActividadForm()

        return render(request, 'formularios/actividadCrear.html', {
            'form': form,
            'asignatura': asignatura,
        })

def actividadListar(request):
    if request.session.get("logueado"):
        actividades = Actividad.objects.all() 
        return render(request, 'formularios/actividadListar.html', {'actividades': actividades})

def actividadListar1(request):
    if request.session.get("logueado", {}).get("rol") == "ADM" :
        actividad = list(Actividad.objects.values())
        data = {'actividad': actividad}
        return JsonResponse(data)
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index") 

def actividadActualizar(request, actividad_id):
    if request.session.get("logueado", {}).get("rol") == "ADM" or "PROF" :
        actividad = get_object_or_404(Actividad, id=actividad_id)
        if request.method == "POST":
            form = ActividadForm(request.POST, instance=actividad)
            if form.is_valid():
                form.save()
                return redirect('asignaturasListar')
        else:
            form = ActividadForm(instance=actividad)
        return render(request, 'formularios/actividadActualizar.html', {'form': form})

def actividadEliminar(request, actividad_id):
    if request.session.get("logueado", {}).get("rol")  in ["ADM", "PROF"]:
        actividad = get_object_or_404(Actividad, id=actividad_id)
        if request.method == "POST":
            actividad.delete()
            return redirect('actividadListar')
        return render(request, 'formularios/actividadEliminar.html', {'actividad': actividad})

def actividadesPorAsignatura(request, asignatura_id):
    
    asignatura = get_object_or_404(Asignatura, id=asignatura_id)
    actividades = asignatura.actividades.all()
    return render(request, 'formularios/actividadesPorAsignatura.html', {
        'asignatura': asignatura,
        'actividades': actividades
    })

#Notas de Actividades
from django.contrib import messages

def crearNota(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    estudiantes = actividad.asignatura.grados.estudiantes.all()
    errores = False

    if request.method == 'POST':
        porcentaje_general = request.POST.get('porcentaje_general')

        try:
            porcentaje_general = float(porcentaje_general)
            if not (5 <= porcentaje_general <= 100):
                messages.error(request, "El porcentaje general debe estar entre 5 y 100.")
                errores = True
        except (ValueError, TypeError):
            messages.error(request, "Porcentaje general inválido.")
            errores = True

        if not errores:
            for estudiante in estudiantes:
                nota_key = f'nota_{estudiante.id}'
                nota_valor = request.POST.get(nota_key)

                if nota_valor is not None and nota_valor.strip() != "":
                    try:
                        nota_valor = float(nota_valor)
                        if 0 <= nota_valor <= 5:
                            nota_obj, created = Nota.objects.get_or_create(
                                actividad=actividad,
                                estudiante=estudiante,
                                defaults={'valor': nota_valor, 'porcentaje': porcentaje_general}
                            )
                            if not created:
                                nota_obj.valor = nota_valor
                                nota_obj.porcentaje = porcentaje_general
                                nota_obj.save()
                        else:
                            errores = True
                            messages.error(request, f"La nota de {estudiante.usuario.nombre} debe estar entre 0 y 5.")
                    except ValueError:
                        errores = True
                        messages.error(request, f"Nota inválida para {estudiante.usuario.nombre}.")

            if not errores:
                messages.success(request, "Notas guardadas exitosamente.")

        # Al final del POST, renderiza la misma vista
        notas_actuales = {nota.estudiante.id: nota for nota in Nota.objects.filter(actividad=actividad)}

        return render(request, 'formularios/notasCrear.html', {
            'actividad': actividad,
            'estudiantes': estudiantes,
            'notas_actuales': notas_actuales,
        })

    # Prepara notas existentes para el template
    notas_actuales = {
        nota.estudiante.id: nota
        for nota in Nota.objects.filter(actividad=actividad)
    }

    context = {
        'actividad': actividad,
        'estudiantes': estudiantes,
        'notas_actuales': notas_actuales,
    }
    return render(request, 'formularios/notasCrear.html', context)




#Blogs
def blogsCrear(request):
    if request.session.get("logueado", {}).get("rol")  in ["ADM", "PROF"]:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('blogsListar')
        else:
            form = BlogForm()
        return render(request, 'formularios/blogsCrear.html', {'form': form})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")

def blogsListar(request):
    if request.session.get("logueado"):
        blogs = Blog.objects.all()
        return render(request, 'formularios/blogsListar.html', {'blogs': blogs})
    else:
        messages.warning(request, "No tienes permiso para modificar este usuario.")
        return redirect("index")
    
def blogsListar1(request):
    sesion = request.session.get("logueado", {})
    rol = sesion.get("rol")
    usuario_id = sesion.get("id")

    if rol not in ["ADM", "PROF", "EST"]:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    if not usuario_id:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    blogs = Blog.objects.select_related('grados', 'actividad__asignatura__profesor__usuario')

    if rol == "ADM":
        blogs_filtrados = blogs.all()

    elif rol == "PROF":
        try:
            profesor = Profesor.objects.get(usuario=usuario)
            blogs_filtrados = blogs.filter(actividad__asignatura__profesor=profesor)
        except Profesor.DoesNotExist:
            return JsonResponse({'error': 'Profesor no registrado'}, status=404)

    elif rol == "EST":
        try:
            estudiante = Estudiante.objects.select_related('grado').get(usuario=usuario)
            blogs_filtrados = blogs.filter(grados=estudiante.grado)
        except Estudiante.DoesNotExist:
            return JsonResponse({'error': 'Estudiante no registrado'}, status=404)

    else:
        blogs_filtrados = Blog.objects.none()

    data = {
        'usuario': {
            'rol': rol
        },
        'blogs': [
            {
                'id': blog.id,
                'titulo': blog.titulo,
                'grados': blog.grados.nombre if blog.grados else "",
                'actividad': blog.actividad.nombre if blog.actividad else "",
                'contenido': blog.contenido,
                'fechaCreacion': blog.fechaCreacion.strftime("%Y-%m-%d"),
            }
            for blog in blogs_filtrados
        ]
    }

    return JsonResponse(data)

def blogsActualizar(request, blog_id):
    if request.session.get("logueado", {}).get("rol") == "ADM" or request.session.get("logueado", {}).get("rol") == "PROF":
        blog = get_object_or_404(Blog, id=blog_id)
        if request.method == 'POST':
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
                return redirect('blogsListar')
        else:
            form = BlogForm(instance=blog)
        return render(request, 'formularios/blogsActualizar.html', {'form': form, 'blog': blog})

def blogsEliminar(request, blog_id):
    if request.session.get("logueado", {}).get("rol") == "ADM" or request.session.get("logueado", {}).get("rol") == "PROF":
        blog = get_object_or_404(Blog, id=blog_id)
        if request.method == 'POST':
            blog.delete()
            return redirect('blogsListar')
        return render(request, 'formularios/blogsEliminar.html', {'blog': blog})
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index, name="index"),
    path("principal/",views.principal, name="principal"),
    path("login/",views.login, name="login"),
    path("registrarUsuarios/",views.registrarUsuarios, name="registrarUsuarios"),
    path("perfil/",views.perfil, name="perfil"),
    path("cambioPassword/",views.cambioPassword, name="cambioPassword"),
    path("recuperarPassword/",views.recuperarPassword, name="recuperarPassword"),
    path("verificar_token_recuperar_password/",views.token, name="verificar_token_recuperar_password"),
    path("logout/", views.logout , name="logout"),
    path("editarFotoPerfil/", views.editarFotoPerfil , name="editarFotoPerfil"),
    
    #Usuarios
    path('usuariosEliminar/<int:id>/', views.usuariosEliminar, name='usuariosEliminar'),
    path('modificarUsuario/<int:id>/', views.modificarUsuario, name='modificarUsuario'),
    path('perfilUsuario/<int:id>/', views.perfilUsuario, name='perfilUsuario'),
    path('usuariosListar/', views.usuariosListar, name='usuariosListar'),
    path('usuariosListar1/', views.usuariosListar1, name='usuariosListar1'),
    
    #Grados
    path('gradosCrear', views.gradosCrear, name='gradosCrear'),
    path('gradosActualizar/<int:grupo_id>/', views.gradosActualizar, name='gradosActualizar'),
    path('gradosEliminar/<int:grupo_id>/', views.gradosEliminar, name='gradosEliminar'),
    path('gradosListar/', views.gradosListar, name='gradosListar'),
    path('gradosListar1/', views.gradosListar1, name='gradosListar1'),
        
    #Asignaturas
    path('asignaturasListar/', views.asignaturasListar, name='asignaturasListar'),
    path('asignaturasListar1/', views.asignaturasListar1, name='asignaturasListar1'), 
    path('asignaturasCrear', views.asignaturasCrear, name='asignaturasCrear'),
    path('asignaturasActualizar/<int:id>/', views.asignaturasActualizar, name='asignaturasActualizar'),
    path('asignaturasEliminar/<int:id>/', views.asignaturasEliminar, name='asignaturasEliminar'),
    path('asignaturas/<int:asignatura_id>/actividades/', views.actividadesPorAsignatura, name='actividadesPorAsignatura'),
    
    #Actividades
    path('asignaturas/<int:asignatura_id>/actividadCrear/', views.actividadCrear, name='actividadCrear'),
    path('actividadListar/', views.actividadListar, name='actividadListar'),
    path('actividadListar1/', views.actividadListar1, name='actividadListar1'),
    path('actividadActualizar/<int:actividad_id>/', views.actividadActualizar, name='actividadActualizar'),
    path('actividadEliminar/<int:actividad_id>/', views.actividadEliminar, name='actividadEliminar'),
    
    #Notas Actividades
   


    #Estudiantes
    path('estudiantesListar/', views.estudiantesListar, name='estudiantesListar'),
    path('usuariosListar2/', views.usuariosListar2, name='usuariosListar2'),
    
    #Blogs
    path('blogCrear/', views.blogsCrear, name='blogsCrear'),
    path('blogsListar/', views.blogsListar, name='blogsListar'),
    path('blogsListar1/', views.blogsListar1, name='blogsListar1'),
    path('blogsActualizar/<int:blog_id>/', views.blogsActualizar, name='blogsActualizar'),
    path('blogsEliminar/<int:blog_id>/', views.blogsEliminar, name='blogsEliminar'),
    
]   


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
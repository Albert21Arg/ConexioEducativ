from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Usuario, Estudiante, Profesor

@receiver(pre_save, sender=Usuario)
def eliminar_rol_anterior(sender, instance, **kwargs):
    if instance.pk:
        usuario_anterior = Usuario.objects.get(pk=instance.pk)
        rol_anterior = usuario_anterior.rol
        rol_actual = instance.rol

        if rol_anterior != rol_actual:
            if rol_anterior == 'EST':
                try:
                    usuario_anterior.estudiante.delete()
                except Estudiante.DoesNotExist:
                    pass
            elif rol_anterior == 'PROF':
                try:
                    usuario_anterior.profesor.delete()
                except Profesor.DoesNotExist:
                    pass

@receiver(post_save, sender=Usuario)
def crear_rol_usuario(sender, instance, created, **kwargs):
    if instance.rol == 'EST':
        Estudiante.objects.get_or_create(usuario=instance)
    elif instance.rol == 'PROF':
        Profesor.objects.get_or_create(usuario=instance)

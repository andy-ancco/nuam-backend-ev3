from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Auditoria, Certificado, Calificacion, Usuario

def log(usuario, accion):
    Auditoria.objects.create(usuario=usuario if usuario and usuario.is_authenticated else None, accion=accion)

# Login exitoso
@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    log(user, f"Inicio de sesión exitoso")

# Logout
@receiver(user_logged_out)
def logout_success(sender, request, user, **kwargs):
    log(user, f"Cerró sesión")

# Intento fallido
@receiver(user_login_failed)
def login_failed(sender, credentials, **kwargs):
    log(None, f"Intento fallido de login con usuario: {credentials.get('username')}")


# Subida / modificación certificados
@receiver(post_save, sender=Certificado)
def certificado_guardado(sender, instance, created, **kwargs):
    # Evitar errores si aún no tiene usuario asignado
    if hasattr(instance, "usuario") and instance.usuario is not None:
        log(
            instance.usuario,
            f"{'Subió' if created else 'Modificó'} un certificado: {instance.titulo}"
        )


# Eliminación certificado
@receiver(post_delete, sender=Certificado)
def certificado_eliminado(sender, instance, **kwargs):
    log(instance.usuario, f"Eliminó un certificado: {instance.titulo}")

# CONTROL DE PERMISOS -> detecta cambios de rol
@receiver(pre_save, sender=Usuario)
def cambio_permiso(sender, instance, **kwargs):
    if instance.pk:
        old_user = Usuario.objects.get(pk=instance.pk)
        if old_user.rol != instance.rol:
            log(instance, f"Cambio de rol: {old_user.rol} → {instance.rol}")

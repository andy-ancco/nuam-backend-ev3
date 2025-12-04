from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from .validators import validar_extension_archivo


class Usuario(AbstractUser):
    ROLES = [
        ("ADMIN", "Administrador"),
        ("EMPLEADO", "Empleado NUAM"),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default="EMPLEADO")
    activo = models.BooleanField(default=True)


class Calificacion(models.Model):
    # Calificación tributaria asociada a un cliente (usuario)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Calificación {self.id} - {self.usuario.username} - {self.puntaje}"


class Certificado(models.Model):
    # 🔁 AHORA el certificado se asocia a una CALIFICACIÓN, no al empleado NUAM
    calificacion = models.ForeignKey(
        Calificacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="certificados"
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    archivo = models.FileField(
        upload_to="certificados/",
        validators=[validar_extension_archivo]
    )

    fecha_emision = models.DateField(null=True, blank=True)   # Opcional
    fecha_subida = models.DateTimeField(auto_now_add=True)    # Cuando se sube a NUAM

    validado = models.BooleanField(default=False)  # Revisión por administrador

    def __str__(self):
        if self.calificacion and self.calificacion.usuario:
            return f"{self.titulo} - Cliente: {self.calificacion.usuario.username}"
        return f"{self.titulo} - Sin calificación asociada"


class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha}"


class Documento(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict)
    archivo = models.FileField(
        upload_to="documentos/",
        validators=[validar_extension_archivo]
    )
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

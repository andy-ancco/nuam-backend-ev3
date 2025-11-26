from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [
        ("ADMIN", "Administrador NUAM"),
        ("EMPLEADO", "Empleado NUAM"),
        ("INVERS", "Inversionista NUAM"),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default="EMPLEADO")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

class Calificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class Certificado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_emision = models.DateField(auto_now_add=True)
    archivo_pdf = models.FileField(upload_to="certificados/")

class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=200)
    tabla = models.CharField(max_length=100)
    detalle = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)

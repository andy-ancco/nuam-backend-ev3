from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class Usuario(AbstractUser):
    ROLES = [
        ("ADMIN", "Administrador"),
        ("EMPLEADO", "Empleado NUAM"),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default="EMPLEADO")
    activo = models.BooleanField(default=True)

class Calificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class Certificado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo_pdf = models.FileField(upload_to="certificados/")
    fecha_emision = models.DateField(auto_now_add=True)

class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

class Documento(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict) 
    archivo = models.FileField(upload_to="documentos/")
    creado = models.DateTimeField(auto_now_add=True)
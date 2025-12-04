from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Usuario, Certificado, Calificacion, Auditoria, Documento
from .serializers import (
    UsuarioSerializer,
    CertificadoSerializer,
    CalificacionSerializer,
    AuditoriaSerializer,
    DocumentoSerializer
)
from .permissions import IsAdmin, IsEmpleadoOrAdmin


# 👨‍💼 Solo el Admin puede gestionar usuarios
class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]


# 📄 Certificados (Empleado puede subir/editar/eliminar y VALIDAR los suyos)
class CertificadoViewSet(ModelViewSet):
    serializer_class = CertificadoSerializer
    permission_classes = [IsAuthenticated, IsEmpleadoOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.rol == "ADMIN":
            return Certificado.objects.all()

        # Empleado solo ve certificados asociados a sus calificaciones o pendientes
        qs_propios = Certificado.objects.filter(calificacion__usuario=user)
        qs_sin_calificacion = Certificado.objects.filter(calificacion__isnull=True)
        return qs_propios | qs_sin_calificacion

    def perform_create(self, serializer):
        instancia = serializer.save()
        Auditoria.objects.create(
            usuario=self.request.user,
            accion=f"Subió un certificado: {instancia.titulo}"
        )

    def perform_update(self, serializer):
        instancia = self.get_object()
        user = self.request.user

        if user.rol != "ADMIN":
            if instancia.validado:
                raise PermissionDenied("⛔ No puedes modificar un certificado validado.")
            if instancia.calificacion and instancia.calificacion.usuario != user:
                raise PermissionDenied("⛔ No puedes modificar un certificado de otro usuario.")

        serializer.save()

    def perform_destroy(self, instance=None):
        instancia = self.get_object()
        user = self.request.user

        if user.rol != "ADMIN":
            if instancia.validado:
                raise PermissionDenied("⛔ No puedes eliminar un certificado validado.")
            if instancia.calificacion and instancia.calificacion.usuario != user:
                raise PermissionDenied("⛔ No puedes eliminar un certificado de otro usuario.")

        instancia.delete()

    # 🟣 VALIDAR CERTIFICADO (Solo empleado)
    @action(detail=True, methods=["post"])
    def validar(self, request, pk=None):
        certificado = self.get_object()

        # ❌ No volver a validar
        if certificado.validado:
            raise PermissionDenied("⚠ Este certificado ya está validado.")

        # ❌ ADMIN no valida por ahora
        if request.user.rol == "ADMIN":
            raise PermissionDenied("⛔ El administrador no puede validar certificados en esta etapa.")

        # ✔ Solo empleado valida certificados ligados a sus calificaciones
        if not certificado.calificacion or certificado.calificacion.usuario != request.user:
            raise PermissionDenied("⛔ Solo puedes validar certificados asociados a tu trabajo.")

        certificado.validado = True
        certificado.save()

        Auditoria.objects.create(
            usuario=request.user,
            accion=f"Validó el certificado: {certificado.titulo}"
        )

        return Response({"status": "validado", "id": certificado.id})


# ⭐ Calificaciones (por ahora solo lectura para el empleado)
class CalificacionViewSet(ReadOnlyModelViewSet):
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, IsEmpleadoOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.rol == "ADMIN":
            return Calificacion.objects.all()
        return Calificacion.objects.filter(usuario=user)


# 📂 Documentos (Empleado puede subir/editar/eliminar solo los suyos)
class DocumentoViewSet(ModelViewSet):
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated, IsEmpleadoOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.rol == "ADMIN":
            return Documento.objects.all()
        return Documento.objects.filter(usuario=user)

    def perform_create(self, serializer):
        instancia = serializer.save(usuario=self.request.user)
        Auditoria.objects.create(
            usuario=self.request.user,
            accion=f"Subió un documento: {instancia.titulo}"
        )

    def perform_update(self, serializer):
        instancia = self.get_object()
        if instancia.usuario != self.request.user and self.request.user.rol != "ADMIN":
            raise PermissionDenied("⛔ No puedes modificar un documento que no es tuyo.")
        serializer.save()

    def perform_destroy(self, instance=None):
        instancia = self.get_object()
        if instancia.usuario != self.request.user and self.request.user.rol != "ADMIN":
            raise PermissionDenied("⛔ No puedes eliminar un documento que no es tuyo.")
        instancia.delete()


# 🕵️ Auditoría (Empleado solo puede ver lo suyo, Admin ve todo)
class AuditoriaViewSet(ReadOnlyModelViewSet):
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAuthenticated, IsEmpleadoOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.rol == "ADMIN":
            return Auditoria.objects.all()
        return Auditoria.objects.filter(usuario=user)


# 👤 Endpoint para obtener información del usuario logueado
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def user_info(request):
    return Response({
      "id": request.user.id,
      "username": request.user.username,
      "rol": request.user.rol,
      "email": request.user.email
    })

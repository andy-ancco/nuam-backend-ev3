from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Usuario, Certificado, Calificacion, Auditoria
from .serializers import (
    UsuarioSerializer,
    CertificadoSerializer,
    CalificacionSerializer,
    AuditoriaSerializer
)

# Importamos permisos personalizados
from .permissions import IsAdmin, IsEmpleado


# ---------------------- VIEWSETS CON PERMISOS ---------------------- #

class UsuarioViewSet(ModelViewSet):
    """Solo el administrador puede ver, editar o eliminar usuarios."""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]


class CertificadoViewSet(ModelViewSet):
    """Empleado y Admin pueden gestionar certificados."""
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer
    permission_classes = [IsAuthenticated, (IsEmpleado | IsAdmin)]


class CalificacionViewSet(ModelViewSet):
    """Empleado y Admin pueden gestionar calificaciones."""
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, (IsEmpleado | IsAdmin)]


class AuditoriaViewSet(ModelViewSet):
    """Solo el administrador puede acceder a auditorías."""
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAdmin]


# ---------------------- ENDPOINT EXTRA ---------------------- #

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    """Retorna información del usuario autenticado."""
    return Response({
        "username": request.user.username,
        "rol": request.user.rol,
        "email": request.user.email
    })

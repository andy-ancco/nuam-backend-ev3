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

from .permissions import IsAdmin, IsEmpleadoOrAdmin


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdmin]


class CertificadoViewSet(ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer
    permission_classes = [IsAuthenticated, IsEmpleadoOrAdmin]


class CalificacionViewSet(ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated, IsEmpleadoOrAdmin]


class AuditoriaViewSet(ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer
    permission_classes = [IsAdmin]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "rol": request.user.rol,
        "email": request.user.email
    })

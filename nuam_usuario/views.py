from rest_framework.viewsets import ModelViewSet
from .models import Usuario, Certificado, Calificacion, Auditoria
from .serializers import UsuarioSerializer, CertificadoSerializer, CalificacionSerializer, AuditoriaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class CalificacionViewSet(ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer

class CertificadoViewSet(ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer

class AuditoriaViewSet(ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer

@api_view(["GET"])
def user_info(request):
    return Response({
        "username": request.user.username,
        "rol": request.user.rol,
        "email": request.user.email
    })

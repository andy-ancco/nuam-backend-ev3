from rest_framework import serializers
from .models import Usuario, Calificacion, Certificado, Auditoria


# --------------------------
# 🟦 Usuario
# --------------------------
class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = "__all__"
        read_only_fields = ["last_login", "date_joined"]


# --------------------------
# 🟩 Calificación
# --------------------------
class CalificacionSerializer(serializers.ModelSerializer):

    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name",
        read_only=True
    )

    class Meta:
        model = Calificacion
        fields = "__all__"


# --------------------------
# 🟧 Certificado
# --------------------------
class CertificadoSerializer(serializers.ModelSerializer):

    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name",
        read_only=True
    )

    class Meta:
        model = Certificado
        fields = "__all__"


# --------------------------
# 🟥 Auditoría
# --------------------------
class AuditoriaSerializer(serializers.ModelSerializer):

    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name",
        read_only=True
    )

    class Meta:
        model = Auditoria
        fields = "__all__"

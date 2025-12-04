from rest_framework import serializers
from .models import Usuario, Calificacion, Certificado, Auditoria, Documento


class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source="get_full_name", read_only=True)

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
        read_only_fields = ["usuario", "fecha"]  # empleado no define esto


# --------------------------
# 🟧 Certificado (de cliente, ligado a calificación)
# --------------------------
class CertificadoSerializer(serializers.ModelSerializer):
    # nombre del cliente al que pertenece la calificación
    cliente_nombre = serializers.CharField(
        source="calificacion.usuario.get_full_name",
        read_only=True
    )

    class Meta:
        model = Certificado
        fields = "__all__"
        # ❗ ya no hay usuario aquí; lo controla el backend/admin
        read_only_fields = ["validado", "fecha_subida"]


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
        read_only_fields = ["usuario", "fecha"]


# --------------------------
# 📤 Documento
# --------------------------
class DocumentoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name",
        read_only=True
    )

    class Meta:
        model = Documento
        fields = "__all__"
        read_only_fields = ["usuario", "creado"]

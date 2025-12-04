import os
from django.core.exceptions import ValidationError

# Extensiones permitidas
EXTENSIONES_PERMITIDAS = [
    ".pdf", ".png", ".jpg", ".jpeg",
    ".docx", ".xlsx", ".xls", ".zip"
]

def validar_extension_archivo(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        raise ValidationError(
            f"❌ Extensión no permitida: '{ext}'. "
            f"Extensiones permitidas: {', '.join(EXTENSIONES_PERMITIDAS)}"
        )

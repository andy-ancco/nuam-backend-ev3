from pathlib import Path
import os
from datetime import timedelta
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = "django-insecure-123-change-this"
DEBUG = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]
CORS_ALLOW_CREDENTIALS = True
# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://tudominio.onrender.com",  
]

# App principal (Django + REST + JWT)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicaciones locales
    "nuam_usuario.apps.NuamUsuarioConfig",
    "nuam_admin",

    # Dependencias externas
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs principales
ROOT_URLCONF = "nuam_sistema.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "nuam_sistema.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DBNAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("DB_PORT"),
        "OPTIONS": {
            "sslmode": "require"
        }
    }
}


# Sistema de usuarios personalizado
AUTH_USER_MODEL = "nuam_usuario.Usuario"

# JWT + DRF Config
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Archivos estáticos
STATIC_URL = "static/"

# Default PK
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

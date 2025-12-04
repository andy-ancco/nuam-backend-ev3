from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UsuarioViewSet,CertificadoViewSet,CalificacionViewSet,AuditoriaViewSet,DocumentoViewSet,user_info,  # ✔ IMPORTADO
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet)  # OK
router.register("certificados", CertificadoViewSet, basename="certificados")
router.register("calificaciones", CalificacionViewSet, basename="calificaciones")
router.register("auditorias", AuditoriaViewSet, basename="auditorias")
router.register("documentos", DocumentoViewSet, basename="documentos")


urlpatterns = [
    path("", include(router.urls)),
    path("me/", user_info),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
]

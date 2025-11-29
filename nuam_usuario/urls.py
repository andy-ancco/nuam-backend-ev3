from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet)
router.register("certificados", CertificadoViewSet)
router.register("calificaciones", CalificacionViewSet)
router.register("auditorias", AuditoriaViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("me/", user_info), 
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

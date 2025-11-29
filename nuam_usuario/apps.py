from django.apps import AppConfig


class NuamUsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nuam_usuario'

    def ready(self):
        import nuam_usuario.signals

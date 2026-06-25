from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Importar el paquete de módulos hace que cada uno se registre solo.
        from . import modules  # noqa: F401

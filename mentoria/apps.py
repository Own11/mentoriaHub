from django.apps import AppConfig


class MentoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentoria'
    def ready(self):
        # Import signals to ensure UserProfile is created when User is created
        try:
            import mentoria.signals  # noqa: F401
        except Exception:
            pass

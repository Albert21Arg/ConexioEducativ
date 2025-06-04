from django.apps import AppConfig


class MycolegiodjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myColegioDjango'

    def ready(self):
        import myColegioDjango.signals
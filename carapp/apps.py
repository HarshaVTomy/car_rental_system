from django.apps import AppConfig


class CarappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carapp'

    def ready(self):
        import carapp.signals 

from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    # label = 'myapp_label'  # Unique label


    def ready(self):
        import myapp.signals  
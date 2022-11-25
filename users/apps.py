from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Although you can’t import models at the module-level where AppConfig classes are defined, you can import them in ready(), using either an import statement or get_model().
    def ready(self):
        import users.signals

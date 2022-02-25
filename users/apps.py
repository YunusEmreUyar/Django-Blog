from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "Kullanıcılar"
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import users.signals

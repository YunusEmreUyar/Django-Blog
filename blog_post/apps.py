from django.apps import AppConfig


class BlogPostConfig(AppConfig):
    name = 'Blog'
    verbose_name = "Blog / Gönderiler"
    default_auto_field = 'django.db.models.BigAutoField'

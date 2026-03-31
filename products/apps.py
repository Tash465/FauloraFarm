from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from django.contrib.auth.models import User

        def create_admin(sender, **kwargs):
            username = 'T490s9'
            password = '27962@Ikingi'
            email = 'talianyaga6@gmail.com'

            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)

        post_migrate.connect(create_admin, sender=self)
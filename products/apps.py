from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        # This code runs once when the app starts
        from django.contrib.auth.models import User
        username = 'T490s9'   
        password = '27962@Ikingi'  
        email = 'talianyaga6@gmail.com'

        # Check if the user already exists
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
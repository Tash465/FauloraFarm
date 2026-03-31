from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create Render superuser if it does not exist'

    def handle(self, *args, **options):
        username = 'T490s9'
        password = '27962@Ikingi'
        email = 'talianyaga6@gmail.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))
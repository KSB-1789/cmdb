from django.core.management.base import BaseCommand
from profiles.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Creates an admin user'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
        else:
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin user created successfully.'))
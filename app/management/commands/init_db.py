from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile
import os


class Command(BaseCommand):
    help = 'Initialize database with migrations and create superuser if needed'

    def handle(self, *args, **options):
        # Check if superuser exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.SUCCESS('✓ Superuser already exists'))
        else:
            # Create superuser
            admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', admin_password)
            
            # Create profile for superuser
            Profile.objects.get_or_create(user=admin_user)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Superuser created with username: admin')
            )
            self.stdout.write(f'  Password: {admin_password}')

        # Create a demo user if it doesn't exist
        if not User.objects.filter(username='demo').exists():
            demo_user = User.objects.create_user('demo', 'demo@example.com', 'demo123')
            Profile.objects.get_or_create(user=demo_user)
            self.stdout.write(self.style.SUCCESS('✓ Demo user created'))
            self.stdout.write('  Username: demo')
            self.stdout.write('  Password: demo123')
        else:
            self.stdout.write(self.style.SUCCESS('✓ Demo user already exists'))

        self.stdout.write(self.style.SUCCESS('\n✓ Database initialization complete!'))

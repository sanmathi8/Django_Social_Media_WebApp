import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Profile

# Create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass')
    user.save()
    print(f"Created user: {user.username}")
else:
    print(f"User {user.username} already exists")

# Create a profile if it doesn't exist
profile, created = Profile.objects.get_or_create(user=user)
print(f"Profile exists: {not created}")

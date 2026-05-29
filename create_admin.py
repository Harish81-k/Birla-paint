import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Birla.settings')
django.setup()

from django.contrib.auth.models import User

# Configuration for your Admin Account
USERNAME = 'admin'
EMAIL = 'harish@example.com'
PASSWORD = 'Harish@12'  # Change this to whatever password you want

if not User.objects.filter(username=USERNAME).exists():
    print(f"Creating superuser account for {USERNAME}...")
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print("Superuser created successfully!")
else:
    print(f"Superuser '{USERNAME}' already exists. Updating password...")
    user = User.objects.get(username=USERNAME)
    user.set_password(PASSWORD)
    user.save()
    print("Password updated successfully!")
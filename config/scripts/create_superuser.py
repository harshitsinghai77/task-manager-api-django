import os
import sys
import django

# Set the path to the project root (adjust as needed)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # update if your settings module differs
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = "user"
email = "admin@example.com"
password = "password"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")

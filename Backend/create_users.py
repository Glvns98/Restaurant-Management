import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurant_management_system.settings')
django.setup()

from django.contrib.auth.models import User, Group

def create_user(username, password, group_name=None, is_superuser=False):
    if not User.objects.filter(username=username).exists():
        if is_superuser:
            user = User.objects.create_superuser(username=username, password=password, email=f"{username}@example.com")
        else:
            user = User.objects.create_user(username=username, password=password, email=f"{username}@example.com")
        
        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        print(f"Created user: {username}")
    else:
        print(f"User {username} already exists")

# Admin login: username:"dkp" password:"Dkp@4321"
create_user("dkp", "Dkp@4321", is_superuser=True)

# Employee login: username:"admin" password:"123456789"
create_user("admin", "123456789", group_name="Tier 2 - Restaurant Manager")

# Customer login: username:"user" password:"user"
create_user("user", "user", group_name="Tier 5 - Customer")

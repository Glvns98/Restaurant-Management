import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Restaurant_management_system.settings")
django.setup()

from django.contrib.auth.models import User
from shop.models import UserProfile

def create_admin():
    username = "admin"
    password = "123456"
    email = "admin@foodmania.com"
    
    # Delete old "Admin" if it exists
    if User.objects.filter(username="Admin").exists():
        User.objects.filter(username="Admin").delete()
        print("Deleted old 'Admin' account.")
    
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Updating password and role...")
        user = User.objects.get(username=username)
    else:
        print(f"Creating master admin account '{username}'...")
        user = User.objects.create_user(username=username, email=email)
        
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    # Update or create profile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'ADMIN'
    profile.save()
    print("Master admin account seeded successfully!")

if __name__ == "__main__":
    create_admin()

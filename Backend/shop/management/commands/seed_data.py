import random
import json
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Restaurant, Product
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds the database with the exact product list and categories provided by the user.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding user-defined data...")

        # Create a default user and restaurant if they don't exist
        user, _ = User.objects.get_or_create(username='admin_seeder', email='admin@thefoodmania.com')
        if _:
            user.set_password('password123')
            user.save()

        restaurant, _ = Restaurant.objects.get_or_create(
            name="The Epicurean Hub",
            defaults={'location': '123 Main St', 'owner': user}
        )

        # Exact product list from user
        # Format: (name, category, price)
        user_products = [
            ("Water", "Drinks", 1500),
            ("Sprite", "Drinks", 2000),
            ("Coca Cola", "Drinks", 2000),
            ("Thums Up", "Drinks", 2000),
            ("Ultimate Cheesecake Frappe", "Coffee", 12000),
            ("Crunchy Frappe", "Coffee", 12500),
            ("Cold Devils Own", "Coffee", 10000),
            ("Turmeric Ginger King Cappuccino", "Coffee", 7500),
            ("White Chocolate King Cappuccino", "Coffee", 11000),
            ("Filter Coffee", "Coffee", 159),
            ("King Latte", "Coffee", 189),
            ("Aloo Tikki Burger", "Burger", 59),
            ("Manchow soup", "Appetizers, Starters & Party Food", 99),
            ("Cheese Uttapam", "South Indian", 150),
            ("Paper Dosa", "South Indian", 50),
            ("Masala Uttapa", "South Indian", 100),
            ("Paper Masala Dosa", "South Indian", 135),
            ("Onion Uttapa", "South Indian", 89),
            ("Upama", "South Indian", 70),
            ("Vada Sambhar", "South Indian", 55),
            ("Idli Sambhar", "South Indian", 55),
            ("Veg Cutlet", "Appetizers, Starters & Party Food", 79),
            ("French fries", "Appetizers, Starters & Party Food", 79),
            ("Paneer Chilly", "Appetizers, Starters & Party Food", 125),
            ("Veg Manchurian", "Appetizers, Starters & Party Food", 120),
            ("Punjabi Samosa", "Appetizers, Starters & Party Food", 55),
            ("Khandvi", "Appetizers, Starters & Party Food", 75),
            ("Cream of Broccoli Soup", "Appetizers, Starters & Party Food", 111),
            ("Chicken Pakora", "Appetizers, Starters & Party Food", 149),
            ("Cranberry Brie Bites", "Appetizers, Starters & Party Food", 78),
            ("Crispy Baked Chicken Wings", "Appetizers, Starters & Party Food", 149),
            ("Vegetarian Sausage Rolls", "Appetizers, Starters & Party Food", 99),
            ("Roasted Vegetable Soup", "Appetizers, Starters & Party Food", 124),
            ("Onion Bhaji", "Appetizers, Starters & Party Food", 150),
            ("Coconut Shrimp", "Appetizers, Starters & Party Food", 250),
            ("Non-veg Capsicum pizza", "Pizza", 110),
            ("Capsicum pizza", "Pizza", 75),
            ("Non-veg Margherita pizza", "Pizza", 175),
            ("Margherita pizza", "Pizza", 150),
            ("Non-veg Loaded pizza", "Pizza", 200),
            ("Veg Loaded pizza", "Pizza", 135),
            ("Non-veg Paneer pizza", "Pizza", 170),
            ("Non-veg tomato pizza", "Pizza", 150),
            ("Masala Dosa", "South Indian", 110),
            ("paneer pizza", "Pizza", 18500),
            ("tomato pizza", "Pizza", 25000),
        ]

        # Load reference metadata for images and descriptions
        ref_prods = {}
        ref_path = os.path.join(settings.BASE_DIR, 'reference_products.json')
        if os.path.exists(ref_path):
            for enc in ['utf-16', 'utf-8', 'latin-1']:
                try:
                    with open(ref_path, 'r', encoding=enc) as f:
                        data = json.load(f)
                        for item in data:
                            ref_prods[item['product_name'].lower()] = item
                        break
                except: continue

        # Clear existing products to ensure clean slate for user categories
        Product.objects.all().delete()

        count = 0
        for name, cat, price in user_products:
            ref = ref_prods.get(name.lower(), {})
            desc = ref.get('desc', f"Premium {name} from our {cat} selection.")
            img = ref.get('image', '').replace('shop/images/', 'images/')
            
            # Use original price if provided, otherwise estimate TZS factor
            final_price = float(price)
            if final_price > 500:
                final_price = final_price / 2500.0 # Standardizing to "USD" internally as per project convention
            
            rating = round(random.uniform(4.0, 5.0), 1)
            prep_time = random.choice(["10-15 min", "15-20 min", "20-30 min"])

            Product.objects.create(
                name=name,
                restaurant=restaurant,
                description=desc,
                price=round(final_price, 2),
                category=cat,
                rating=rating,
                preparation_time=prep_time,
                image=img,
                is_available=True
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} user-specified products."))

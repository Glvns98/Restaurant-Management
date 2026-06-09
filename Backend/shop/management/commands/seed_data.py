import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Restaurant, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seeds the database with a high-density, realistic catalog of food items.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create a default user and restaurant if they don't exist
        user, _ = User.objects.get_or_create(username='admin_seeder', email='admin@thefoodmania.com')
        user.set_password('password123')
        user.save()

        restaurant, _ = Restaurant.objects.get_or_create(
            name="The Epicurean Hub",
            defaults={'location': '123 Main St', 'owner': user}
        )

        categories = [
            'Fine Dining', 'Quick Bites', 'Healthy Choices', 
            'Midnight Cravings', 'Trending', 'Desserts', 'Beverages'
        ]
        
        foods = [
            ("Truffle Mushroom Burger", "A gourmet classic cheeseburger on a rustic wooden board with truffle oil.", 18.50, "Quick Bites", "https://lh3.googleusercontent.com/aida-public/AB6AXuDUuIVBHcj7zCXRys67jdX0_5uxaWLFW3NlxOQ80rEV0n_99TgqWnsqPBX2B2Q_x_H8l14-SgfgufjOIFCIbarjye1mfqkeAeZoX6WRDrwa1i2JYCXnL6f-H1rlaxZDddv__PpSc0ONPZzw8V4Dg9O5I2dQx4nu3hM-de719s-ZvPvHOUx6WyPOf61D0KfziATW_vxkdWeNI1_ldWDumZkoTSjW4VFrX2CdfWQJCkMpeXb-Ae_zEcamb2nIlQDD2iOIWysRzc0Wogru"),
            ("Sweet Potato Fries", "Crispy sweet potato fries with garlic aioli.", 6.00, "Quick Bites", "https://lh3.googleusercontent.com/aida-public/AB6AXuCss8SPslqL_NCtXUUF5IcVAAgVzBi6OF0QHu8M0dK4HlYnv8hyWmRwi6MTbNqTOMdiPfDafOh5SGu5blIUZ3rHHkiLD2Kqjlpi2v6VYE5Fio2Rjmt4mnECWYlux5MicLAywbSprwJuFPIhQF1TVyRfv-V5ZIirC89wDHSnC8jmhNTSX9dkBZT1h2SZrYER3RN6e2cRMo-awUQX_Bzr5d-ufUJcMH9SkzZ8hgPPEZ6scy3Ze-uFr9ofly5_haqGrZcVn0AOP1kELPBa"),
            ("Avocado Toast", "Toasted sourdough bread with mashed avocado, cherry tomatoes, and a sprinkle of feta cheese.", 12.00, "Healthy Choices", ""),
            ("Quinoa Salad", "Fresh quinoa with mixed greens, roasted vegetables, and lemon vinaigrette.", 14.50, "Healthy Choices", ""),
            ("Wagyu Steak", "Premium A5 Wagyu beef cooked to perfection, served with asparagus.", 85.00, "Fine Dining", ""),
            ("Lobster Bisque", "Rich and creamy soup made with fresh Maine lobster.", 24.00, "Fine Dining", ""),
            ("Midnight Ramen", "Spicy miso broth with thick noodles, chashu pork, and a soft-boiled egg.", 16.00, "Midnight Cravings", ""),
            ("Loaded Nachos", "Corn tortilla chips topped with melted cheese, jalapeños, sour cream, and guacamole.", 10.50, "Midnight Cravings", ""),
            ("Spicy Tuna Roll", "Fresh tuna with spicy mayo wrapped in seaweed and rice.", 15.00, "Trending", ""),
            ("Margherita Pizza", "Classic Italian pizza with San Marzano tomatoes, fresh mozzarella, and basil.", 18.00, "Trending", ""),
            ("Chocolate Lava Cake", "Warm chocolate cake with a molten center, served with vanilla ice cream.", 9.50, "Desserts", ""),
            ("Mango Smoothie", "Freshly blended mangoes with a touch of honey and yogurt.", 6.50, "Beverages", ""),
            ("Iced Caramel Macchiato", "Espresso with milk, vanilla syrup, and a caramel drizzle.", 5.50, "Beverages", ""),
            ("Beef Tacos", "Three soft corn tortillas filled with seasoned ground beef, lettuce, and cheese.", 11.00, "Quick Bites", ""),
            ("Chicken Caesar Wrap", "Grilled chicken, romaine lettuce, parmesan, and Caesar dressing in a flour tortilla.", 10.00, "Quick Bites", ""),
            ("Açaí Bowl", "Blended açaí topped with granola, fresh berries, and a drizzle of honey.", 13.00, "Healthy Choices", ""),
            ("Seared Scallops", "Pan-seared scallops served over a bed of creamy risotto.", 32.00, "Fine Dining", ""),
            ("Pancakes", "Fluffy buttermilk pancakes topped with maple syrup and butter.", 8.00, "Midnight Cravings", ""),
            ("Pad Thai", "Stir-fried rice noodles with eggs, peanuts, bean sprouts, and your choice of protein.", 14.00, "Trending", ""),
            ("Tiramisu", "Classic Italian dessert made with coffee-soaked ladyfingers and mascarpone cheese.", 8.50, "Desserts", ""),
        ]

        # Generate more combinations to reach ~50
        adjectives = ["Spicy", "Crispy", "Grilled", "Roasted", "Fresh", "Classic", "Premium", "Signature", "Homemade", "Authentic"]
        base_foods = ["Chicken Wings", "Beef Burger", "Pork Ribs", "Vegetable Curry", "Fried Rice", "Noodle Soup", "Fish and Chips", "Pasta Alfredo", "Mushroom Risotto", "Greek Salad"]
        
        for adj in adjectives:
            for base in base_foods:
                if len(foods) >= 55:
                    break
                cat = random.choice(categories)
                name = f"{adj} {base}"
                foods.append((name, f"A delicious {name.lower()} prepared with our secret recipe.", random.uniform(8.0, 45.0), cat, ""))

        count = 0
        for name, desc, price, cat, img in foods:
            rating = round(random.uniform(3.5, 5.0), 1)
            prep_time = random.choice(["10-15 min", "15-20 min", "20-30 min", "30-45 min"])
            is_available = random.random() > 0.1 # 90% availability
            
            prod, created = Product.objects.get_or_create(
                name=name,
                restaurant=restaurant,
                defaults={
                    'description': desc,
                    'price': round(price, 2),
                    'category': cat,
                    'rating': rating,
                    'preparation_time': prep_time,
                    'is_available': is_available
                }
            )
            # Update fields if it already existed but was missing image or new fields
            if img and not prod.image:
                prod.image = img
            prod.rating = rating
            prod.preparation_time = prep_time
            prod.is_available = is_available
            prod.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} products."))

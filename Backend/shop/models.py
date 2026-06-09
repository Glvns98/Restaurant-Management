import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_restaurants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=100, default="", db_index=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(max_length=2000, blank=True, null=True)
    publication_date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to="shop/images", default="", blank=True, null=True)
    rating = models.FloatField(default=4.5)
    preparation_time = models.CharField(max_length=50, default="20-30 min")
    is_available = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Session ' + self.session_id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Orders(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    items_json = models.JSONField(help_text="Stores the ordered items in structured JSON format")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=timezone.now)

    STATUS_CHOICES = [
        (1, 'Order Received'),
        (2, 'Preparing Food'),
        (3, 'Cooking'),
        (4, 'Packaging'),
        (5, 'Rider Assigned'),
        (6, 'Rider Picked Up Order'),
        (7, 'Rider En Route'),
        (8, 'Near Destination'),
        (9, 'Delivered'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    restaurant_lat = models.FloatField(default=-6.7924)
    restaurant_lng = models.FloatField(default=39.2083)
    rider_lat = models.FloatField(default=-6.7924)
    rider_lng = models.FloatField(default=39.2083)
    user_lat = models.FloatField(default=-6.8000)
    user_lng = models.FloatField(default=39.2200)
    eta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.name}"

    class Meta:
        verbose_name_plural = "Orders"

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_of_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'} (Order {self.order.order_id})"

class OrderUpdate(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='updates')
    status_description = models.CharField(max_length=500)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Update for Order {self.order.order_id} - {self.status_description[:20]}"

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150, default="Notification")
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.title}"

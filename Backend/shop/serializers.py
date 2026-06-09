from rest_framework import serializers
from .models import Product, Orders, OrderUpdate, Cart, CartItem, Notification

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'price', 'description', 'publication_date', 'image_url', 'rating', 'preparation_time', 'is_available']
        
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'name') and obj.image.name.startswith('http'):
            return obj.image.name
        elif obj.image:
            return obj.image.url
        return None

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUpdate
        fields = ['id', 'order', 'status_description', 'timestamp']

class OrderSerializer(serializers.ModelSerializer):
    updates = OrderUpdateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Orders
        fields = ['order_id', 'items_json', 'amount', 'name', 'email', 'address', 'city', 'state', 'zip_code', 'phone', 'user', 'timestamp', 'updates', 'status', 'restaurant_lat', 'restaurant_lng', 'rider_lat', 'rider_lng', 'user_lat', 'user_lng', 'eta']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'timestamp']

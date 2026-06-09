from django.test import TestCase
from django.contrib.auth.models import User
from .models import Restaurant, Product, Cart, CartItem, Orders, OrderItem
from rest_framework.test import APIClient
from rest_framework import status
import json

class ShopModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.restaurant = Restaurant.objects.create(name='Test Rest', location='Test Location')
        self.product = Product.objects.create(restaurant=self.restaurant, name='Pizza', category='Food', price=15000.00)

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, 'Pizza')
        self.assertTrue(self.product.is_available)

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)


class ShopAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.restaurant = Restaurant.objects.create(name='Test Rest', location='Test Location')
        self.product = Product.objects.create(restaurant=self.restaurant, name='Pizza', category='Food', price=15000.00)
        self.client.force_authenticate(user=self.user)

    def test_cart_api(self):
        response = self.client.post('/shop/api/cart/', {'action': 'add', 'product_id': self.product.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)

    def test_secure_checkout_api(self):
        # Add to cart first
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # Attempt checkout
        payload = {
            "firstName": "John",
            "lastName": "Doe",
            "address1": "123 Main St",
            "amount": 0 # Malicious payload trying to bypass price
        }
        
        response = self.client.post('/shop/api/checkout/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        order = Orders.objects.first()
        self.assertIsNotNone(order)
        # Server must override the 0 amount with actual price 15000 * 2
        self.assertEqual(order.amount, 30000.00)
        
        # Verify OrderItem relational models are created
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(order.order_items.first().price_at_time_of_order, 15000.00)
        
        # Verify cart is cleared
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_empty_cart_fails(self):
        payload = {"firstName": "John"}
        response = self.client.post('/shop/api/checkout/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Cart is empty')

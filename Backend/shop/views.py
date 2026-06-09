import json
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Orders, OrderUpdate, Contact, Notification, Cart, CartItem, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderUpdateSerializer, NotificationSerializer
import logging
import json
from django.utils import timezone

logger = logging.getLogger(__name__)
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 50

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = Product.objects.all().order_by('-publication_date')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-publication_date')
        
        # Search query
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
            
        # Filters
        category = self.request.query_params.get('category', None)
        if category and category.lower() != 'all':
            queryset = queryset.filter(category__iexact=category)
            
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
            
        prep_time = self.request.query_params.get('prep_time', None)
        if prep_time:
            queryset = queryset.filter(preparation_time__icontains=prep_time)
            
        is_available = self.request.query_params.get('is_available', None)
        if is_available is not None:
            is_avail_bool = is_available.lower() in ['true', '1', 't', 'y', 'yes']
            queryset = queryset.filter(is_available=is_avail_bool)
            
        return queryset

from .models import Cart, CartItem
from .serializers import CartSerializer

class CartAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_id=session_id)
        return cart

    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        action = request.data.get('action') # 'add', 'remove', 'clear'
        
        if action == 'clear':
            cart.items.all().delete()
            return Response(CartSerializer(cart).data)
            
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            
        if action == 'add':
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                item.quantity += 1
                item.save()
        elif action == 'remove':
            try:
                item = CartItem.objects.get(cart=cart, product=product)
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()
            except CartItem.DoesNotExist:
                pass
                
        return Response(CartSerializer(cart).data)

class CheckoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            from .models import Restaurant
            default_restaurant = Restaurant.objects.first()

            import datetime
            eta = timezone.now() + datetime.timedelta(minutes=25)

            # Secure Price Calculation from Cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()
            
            if not cart_items.exists():
                logger.warning(f"Checkout attempted with empty cart for user {request.user.username}")
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            calculated_amount = 0
            items_for_json = []

            for item in cart_items:
                if item.product:
                    calculated_amount += item.product.price * item.quantity
                    items_for_json.append({
                        "id": item.product.id,
                        "name": item.product.name,
                        "qty": item.quantity,
                        "price": str(item.product.price)
                    })

            # Create Order
            order = Orders.objects.create(
                user=request.user,
                restaurant=default_restaurant,
                items_json=json.dumps(items_for_json),
                amount=calculated_amount,
                name=f"{data.get('firstName', '')} {data.get('lastName', '')}",
                email=data.get('email', ''),
                phone=data.get('phone', ''),
                address=data.get('address1', ''),
                city=data.get('city', ''),
                zip_code=data.get('zipCode', ''),
                status=1,
                eta=eta,
                restaurant_lat=-6.7924,
                restaurant_lng=39.2083,
                rider_lat=-6.7924,
                rider_lng=39.2083,
                user_lat=-6.8000,
                user_lng=39.2200
            )

            # Create Order Items for Relational Integrity
            for item in cart_items:
                if item.product:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price_at_time_of_order=item.product.price
                    )

            # Clear the cart
            cart.items.all().delete()

            OrderUpdate.objects.create(order=order, status_description="Order Received")
            Notification.objects.create(user=request.user, title="Order Received", message=f"We have received your order #{order.order_id}.")
            
            logger.info(f"Order #{order.order_id} successfully created for user {request.user.username} with amount {calculated_amount}")
            
            return Response({
                "message": "Order placed successfully", 
                "order_id": order.order_id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error during checkout for user {request.user.username}: {str(e)}")
            return Response({"error": "An error occurred during checkout. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

class TrackerAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return order history
        orders = Orders.objects.filter(user=request.user).order_by('-timestamp')
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        order_id = request.data.get('orderId')
        
        try:
            order = Orders.objects.get(order_id=order_id, user=request.user)
            
            import datetime
            # SIMULATE LIVE TRACKING
            # Every 1 minute elapsed advances 1 state (max 9 states)
            elapsed = timezone.now() - order.timestamp
            minutes = int(elapsed.total_seconds() / 60)
            
            new_status = min(1 + minutes, 9)
            if new_status > order.status:
                order.status = new_status
                status_desc = dict(Orders.STATUS_CHOICES).get(new_status, "Updated")
                OrderUpdate.objects.create(order=order, status_description=status_desc)
                Notification.objects.create(user=request.user, title="Order Update", message=f"Your order #{order.order_id} status changed to: {status_desc}")
                
                # Mock moving the rider if en route (Status 7, 8)
                if new_status >= 7 and new_status < 9:
                    progress = (new_status - 6) / 3.0 # progress from 7 to 8
                    order.rider_lat = order.restaurant_lat + (order.user_lat - order.restaurant_lat) * progress
                    order.rider_lng = order.restaurant_lng + (order.user_lng - order.restaurant_lng) * progress
                elif new_status == 9:
                    order.rider_lat = order.user_lat
                    order.rider_lng = order.user_lng
                
                order.save()
            
            if not order.eta:
                order.eta = order.timestamp + datetime.timedelta(minutes=25)
                order.save()

            updates = order.updates.all().order_by('-timestamp')
            update_data = OrderUpdateSerializer(updates, many=True).data
            
            return Response({
                "status": "success",
                "order": OrderSerializer(order).data,
                "updates": update_data
            })
        except Orders.DoesNotExist:
            return Response({"status": "noitem", "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class NotificationAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = request.user.notifications.all().order_by('-timestamp')
        return Response(NotificationSerializer(notifications, many=True).data)
import json
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Orders, OrderUpdate, Contact, Notification, Cart, CartItem, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderUpdateSerializer, NotificationSerializer, ContactSerializer
import logging
from django.utils import timezone
from PayTm import Checksum

logger = logging.getLogger(__name__)
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
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
        categories = self.request.query_params.getlist('category')
        if categories:
            filtered_cats = [c for c in categories if c.lower() != 'all']
            if filtered_cats:
                cat_query = Q()
                for cat in filtered_cats:
                    cat_query |= Q(category__iexact=cat)
                queryset = queryset.filter(cat_query)
            
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
        
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if action == 'clear':
            cart.items.all().delete()
            return Response(CartSerializer(cart).data)

        if action == 'remove_all':
            CartItem.objects.filter(cart=cart, product=product).delete()
            return Response(CartSerializer(cart).data)
            
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

            subtotal_amount = 0
            items_for_json = []

            for item in cart_items:
                if item.product:
                    subtotal_amount += item.product.price * item.quantity
                    items_for_json.append({
                        "id": item.product.id,
                        "name": item.product.name,
                        "qty": item.quantity,
                        "price": str(item.product.price)
                    })

            service_charge = subtotal_amount * 0.05
            calculated_amount = subtotal_amount + service_charge

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
            
            # Check if user wants online payment
            if data.get('payment_method') == 'online':
                param_dict = {
                    'MID': 'WorldP64425807474247',
                    'ORDER_ID': str(order.order_id),
                    'TXN_AMOUNT': str(calculated_amount),
                    'CUST_ID': request.user.email,
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': 'WEBSTAGING',
                    'CHANNEL_ID': 'WEB',
                    'CALLBACK_URL': 'http://127.0.0.1:8000/shop/api/handlerequest/',
                }
                param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
                return Response({
                    "message": "Redirecting to PayTm", 
                    "order_id": order.order_id,
                    "paytm_params": param_dict
                }, status=status.HTTP_201_CREATED)

            return Response({
                "message": "Order placed successfully", 
                "order_id": order.order_id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error during checkout for user {request.user.username}: {str(e)}")
            return Response({"error": "An error occurred during checkout. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class PayTmHandleRequestAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # paytm will send you post request here
        form = request.data
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                print('order successful')
                order_id = response_dict['ORDER_ID']
                try:
                    order = Orders.objects.get(order_id=order_id)
                    order.status = 2 # Preparing
                    order.save()
                    OrderUpdate.objects.create(order=order, status_description="Payment Successful")
                except Orders.DoesNotExist:
                    pass
            else:
                print('order was not successful because' + response_dict['RESPMSG'])
        
        # In a real app, you'd redirect to a success page or return JSON
        return Response({"status": "verified", "response": response_dict})


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

class ContactAPIView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import UserProfile

class SignUpAPIView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        form = SignUpForm(request.data)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            
            role = form.cleaned_data.get('role', 'CUSTOMER')
            if role == 'ADMIN':
                role = 'CUSTOMER' # Fallback for safety
                
            UserProfile.objects.create(
                user=user, 
                role=role,
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', ''),
                city=form.cleaned_data.get('city', ''),
                state=form.cleaned_data.get('state', ''),
                zip_code=form.cleaned_data.get('zip_code', '')
            )
            
            # Auto-login the user post-registration
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user_auth)
            
            return Response({"message": "User registered successfully", "role": role, "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInAPIView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Note: In a real app, we might also want to verify the role matches, 
        # but usually login is global and role determines destination.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "role": profile.role,
                "username": user.username
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": profile.role,
            "phone": profile.phone,
            "address": profile.address,
            "city": profile.city,
            "state": profile.state,
            "zip_code": profile.zip_code
        })

from django.shortcuts import redirect

class LogoutAPIView(views.APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        logout(request)
        return redirect('/')

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

class AdminDashboardAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.profile.role != 'ADMIN':
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Admin stats
        total_orders = Orders.objects.count()
        total_revenue = sum(o.amount for o in Orders.objects.all())
        total_products = Product.objects.count()
        
        return Response({
            "stats": {
                "total_orders": total_orders,
                "total_revenue": float(total_revenue),
                "total_products": total_products
            }
        })

class SellerDashboardAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.profile.role not in ['ADMIN', 'SELLER']:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Pending orders for sellers
        pending_orders = Orders.objects.filter(status__lt=9).order_by('-timestamp')
        return Response(OrderSerializer(pending_orders, many=True).data)

class NotificationAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = request.user.notifications.all().order_by('-timestamp')
        return Response(NotificationSerializer(notifications, many=True).data)
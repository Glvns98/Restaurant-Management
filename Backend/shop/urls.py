from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    path('api/checkout/', views.CheckoutAPIView.as_view(), name='api-checkout'),
    path('api/tracker/', views.TrackerAPIView.as_view(), name='api-tracker'),
    path('api/cart/', views.CartAPIView.as_view(), name='api-cart'),
    path('api/notifications/', views.NotificationAPIView.as_view(), name='api-notifications'),
    path('api/contact/', views.ContactAPIView.as_view(), name='api-contact'),
    path('api/handlerequest/', views.PayTmHandleRequestAPIView.as_view(), name='api-handlerequest'),
    path('api/signup/', views.SignUpAPIView.as_view(), name='api-signup'),
    path('api/signin/', views.SignInAPIView.as_view(), name='api-signin'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api-profile'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api-logout'),
    path('api/admin/dashboard/', views.AdminDashboardAPIView.as_view(), name='api-admin-dashboard'),
    path('api/seller/dashboard/', views.SellerDashboardAPIView.as_view(), name='api-seller-dashboard'),
]
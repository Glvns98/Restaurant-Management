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
]
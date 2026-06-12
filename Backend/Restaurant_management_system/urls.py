"""Restaurant_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('search/', TemplateView.as_view(template_name='search.html'), name='search'),
    path('checkout/', TemplateView.as_view(template_name='checkout.html'), name='checkout'),
    path('tracker/', TemplateView.as_view(template_name='tracker.html'), name='tracker'),
    path('auth/', TemplateView.as_view(template_name='auth.html'), name='auth'),
    path('admin-dashboard/', TemplateView.as_view(template_name='admin_dashboard.html'), name='admin-dashboard'),
    path('seller-dashboard/', TemplateView.as_view(template_name='seller_dashboard.html'), name='seller-dashboard'),
    
    # Footer Links
    path('about/', TemplateView.as_view(template_name='page.html', extra_context={
        'title': 'About Us', 
        'content': '<h2 class="text-2xl font-bold mb-4">Our Story</h2><p class="mb-4">The Food Mania is dedicated to delivering epicurean modernity straight to your door. We partner with top chefs and local artisans to bring you curated culinary experiences.</p><h3 class="text-xl font-bold mb-2">Our Mission</h3><p class="mb-4">To be the number one choice for modern epicureans, providing bold, bright flavours rooted in the classics with a local twist.</p><h3 class="text-xl font-bold mb-2">Culinary Leadership</h3><p class="mb-4">Our menus, conceived by Chef David Hawksworth and his culinary team, showcase ingredient-led, contemporary cuisine that echoes nostalgia with a modern and local twist.</p>'
    }), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('sustainability/', TemplateView.as_view(template_name='page.html', extra_context={
        'title': 'Sustainability', 
        'content': '<h2 class="text-xl font-bold mb-4">Our Commitment</h2><p class="mb-4">We believe in sustainable food practices. All our packaging is 100% biodegradable and we actively work to reduce our carbon footprint with our delivery fleet.</p>'
    }), name='sustainability'),
    path('partner/', TemplateView.as_view(template_name='page.html', extra_context={
        'title': 'Partner With Us', 
        'content': '<h2 class="text-xl font-bold mb-4">Join the Mania</h2><p class="mb-4">Are you a restaurant looking to expand your reach? Partner with us and get access to our premium delivery network.</p>'
    }), name='partner'),
    path('terms/', TemplateView.as_view(template_name='page.html', extra_context={
        'title': 'Terms of Service', 
        'content': '<h2 class="text-xl font-bold mb-4">Terms</h2><p class="mb-4">By using our service you agree to our standard terms and conditions. Prices are subject to change. Delivery times are estimates.</p>'
    }), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='page.html', extra_context={
        'title': 'Privacy Policy', 
        'content': '<h2 class="text-xl font-bold mb-4">Your Data</h2><p class="mb-4">We take your privacy seriously. Your data is encrypted and never sold to third parties.</p>'
    }), name='privacy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

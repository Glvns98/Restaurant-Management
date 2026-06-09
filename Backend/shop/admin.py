from django.contrib import admin
from .models import Product, Contact, Orders, OrderUpdate, Restaurant

class OrderUpdateInline(admin.TabularInline):
    model = OrderUpdate
    extra = 1
    
    # HARD CONSTRAINT: Prevent deletion of OrderUpdate records
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False # Ensure existing updates cannot be changed, only appended.


class OrdersAdmin(admin.ModelAdmin):
    # Display Order ID, user ID, customer name, email, and timestamp cleanly
    list_display = ('order_id', 'restaurant', 'user', 'name', 'email', 'timestamp')
    list_filter = ['restaurant', 'timestamp']
    search_fields = ['name', 'email', 'order_id']
    inlines = [OrderUpdateInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurant__owner=request.user)

    # HARD CONSTRAINT: Prevent direct modification of Order records by admins.
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in self.model._meta.fields]
        return []

    # HARD CONSTRAINT: Prevent direct addition of Order records by admins.
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'publication_date')
    list_filter = ['restaurant', 'category', 'publication_date']
    search_fields = ['name', 'description', 'category']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurant__owner=request.user)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'timestamp')
    list_filter = ['timestamp']
    search_fields = ['name', 'email', 'phone']

    # HARD CONSTRAINT: Prevent deletion of Contact submissions.
    def has_delete_permission(self, request, obj=None):
        return False

    # HARD CONSTRAINT: Prevent addition of Contact submissions via admin.
    def has_add_permission(self, request):
        return False

    # HARD CONSTRAINT: Prevent modification of Contact submissions.
    def has_change_permission(self, request, obj=None):
        return False


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'created_at')
    list_filter = ['created_at']
    search_fields = ['name', 'location']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

# Register models
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Orders, OrdersAdmin)

# UI Customization: Brand the panel
admin.site.site_header = "The Food Mania Administration"
admin.site.site_title = "The Food Mania Admin Portal"
admin.site.index_title = "Command Center"

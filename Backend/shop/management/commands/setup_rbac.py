from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from shop.models import Restaurant, Product, Orders, OrderUpdate

class Command(BaseCommand):
    help = 'Setup Enterprise RBAC Tiers for Food Mania'

    def handle(self, *args, **kwargs):
        self.stdout.write('Setting up RBAC Tiers...')

        # Fetch Content Types
        restaurant_ct = ContentType.objects.get_for_model(Restaurant)
        product_ct = ContentType.objects.get_for_model(Product)
        orders_ct = ContentType.objects.get_for_model(Orders)
        orderupdate_ct = ContentType.objects.get_for_model(OrderUpdate)

        # Tier 1: Franchise Owner
        tier1, _ = Group.objects.get_or_create(name='Tier 1 - Franchise Owner')
        # Assign all permissions for their own resources (managed via querysets in admin, but they need the global permissions to access the pages)
        tier1.permissions.set(Permission.objects.filter(content_type__in=[restaurant_ct, product_ct, orders_ct, orderupdate_ct]))

        # Tier 2: Restaurant Manager
        tier2, _ = Group.objects.get_or_create(name='Tier 2 - Restaurant Manager')
        # Can manage products, but only view orders and updates
        p_permissions = Permission.objects.filter(content_type=product_ct)
        view_orders = Permission.objects.get(codename='view_orders', content_type=orders_ct)
        view_orderupdate = Permission.objects.get(codename='view_orderupdate', content_type=orderupdate_ct)
        tier2.permissions.set(list(p_permissions) + [view_orders, view_orderupdate])

        # Tier 3: Culinary Staff / Chef
        tier3, _ = Group.objects.get_or_create(name='Tier 3 - Culinary Staff')
        # Can view orders, view updates, add updates, change orders (required to append inline updates in admin)
        change_orders = Permission.objects.get(codename='change_orders', content_type=orders_ct)
        add_orderupdate = Permission.objects.get(codename='add_orderupdate', content_type=orderupdate_ct)
        tier3.permissions.set([view_orders, change_orders, view_orderupdate, add_orderupdate])

        # Tier 4: Front of House / Cashier
        tier4, _ = Group.objects.get_or_create(name='Tier 4 - Front of House')
        # Can view products, add orders, view orders, view updates
        view_product = Permission.objects.get(codename='view_product', content_type=product_ct)
        add_orders = Permission.objects.get(codename='add_orders', content_type=orders_ct)
        tier4.permissions.set([view_product, add_orders, view_orders, view_orderupdate])

        # Tier 5: Customer (Auth)
        tier5, _ = Group.objects.get_or_create(name='Tier 5 - Customer')
        # No admin permissions required; API endpoints handle their access

        self.stdout.write(self.style.SUCCESS('Successfully configured Enterprise RBAC Tiers!'))

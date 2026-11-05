from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import Category, Product

DATA = {
    ('Electronics', 'electronics', '🎧'): [
        ('Wireless Headphones', 'Over-ear Bluetooth headphones with 30-hour battery life and deep bass.', '2499.00', 25),
        ('Smart Watch', 'Fitness tracker with heart-rate monitor, sleep tracking and 7-day battery.', '3299.00', 18),
        ('Portable Power Bank 20000mAh', 'Fast-charging power bank with dual USB output.', '1299.00', 40),
        ('Bluetooth Speaker', 'Waterproof pocket speaker with 12 hours of playtime.', '1799.00', 30),
    ],
    ('Books', 'books', '📚'): [
        ('Python Crash Course', 'A hands-on, project-based introduction to programming with Python.', '599.00', 50),
        ('Clean Code', 'A handbook of agile software craftsmanship by Robert C. Martin.', '749.00', 35),
        ('Introduction to Algorithms', 'The classic reference for algorithms and data structures.', '1299.00', 12),
    ],
    ('Fashion', 'fashion', '👕'): [
        ('Cotton Round-Neck T-Shirt', 'Soft, breathable 100% cotton t-shirt for everyday wear.', '399.00', 100),
        ('Denim Jacket', 'Classic fit denim jacket with button closure.', '1899.00', 15),
        ('Running Shoes', 'Lightweight mesh running shoes with cushioned sole.', '2199.00', 22),
    ],
    ('Home & Kitchen', 'home-kitchen', '🏠'): [
        ('Stainless Steel Bottle 1L', 'Vacuum insulated bottle keeps drinks cold for 24 hours.', '699.00', 60),
        ('Ceramic Coffee Mug Set', 'Set of 4 handcrafted ceramic mugs.', '849.00', 28),
        ('LED Desk Lamp', 'Adjustable desk lamp with three brightness modes and USB port.', '999.00', 0),
    ],
}


class Command(BaseCommand):
    help = 'Load sample categories and products'

    def handle(self, *args, **options):
        created = 0
        for (cname, cslug, icon), items in DATA.items():
            category, _ = Category.objects.get_or_create(slug=cslug, defaults={'name': cname, 'icon': icon})
            for name, desc, price, stock in items:
                slug = name.lower().replace(' ', '-').replace('&', 'and').replace('.', '')
                _, was_created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={'category': category, 'name': name, 'description': desc,
                              'price': Decimal(price), 'stock': stock},
                )
                created += was_created
        self.stdout.write(self.style.SUCCESS(f'Seed complete: {created} new products added.'))

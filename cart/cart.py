from decimal import Decimal

from django.conf import settings

from products.models import Product


class Cart:
    """Session-based shopping cart: {product_id: quantity}."""

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})

    def add(self, product, quantity=1, override=False):
        pid = str(product.id)
        current = 0 if override else self.cart.get(pid, 0)
        self.cart[pid] = max(1, min(current + quantity, product.stock))
        self.save()

    def remove(self, product):
        if str(product.id) in self.cart:
            del self.cart[str(product.id)]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.cart = self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        products = Product.objects.in_bulk([int(i) for i in self.cart])
        for pid, qty in self.cart.items():
            product = products.get(int(pid))
            if product is None:
                continue
            yield {
                'product': product,
                'quantity': qty,
                'price': product.price,
                'total_price': product.price * qty,
            }

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        return sum((item['total_price'] for item in self), Decimal('0'))

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product

from .models import Order


class ShopFlowTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name='Books', slug='books', icon='📚')
        self.product = Product.objects.create(category=cat, name='Python Book', slug='python-book',
                                              price='500.00', stock=5)

    def test_browse_and_detail(self):
        self.assertContains(self.client.get(reverse('products:list')), 'Python Book')
        self.assertContains(self.client.get(self.product.get_absolute_url()), 'In stock')
        self.assertContains(self.client.get(reverse('products:list'), {'q': 'python'}), 'Python Book')

    def test_register_cart_checkout(self):
        resp = self.client.post(reverse('register'), {
            'username': 'divya', 'email': 'd@example.com',
            'password1': 'Str0ngPass!234', 'password2': 'Str0ngPass!234'})
        self.assertRedirects(resp, reverse('products:list'))
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 2})
        self.assertContains(self.client.get(reverse('cart:detail')), '₹1000.00')
        resp = self.client.post(reverse('orders:checkout'), {
            'full_name': 'Divya', 'email': 'd@example.com',
            'address': '12 Main St', 'city': 'Noida', 'postal_code': '201301'})
        order = Order.objects.get()
        self.assertRedirects(resp, reverse('orders:success', args=[order.pk]))
        self.assertEqual(order.get_total_cost(), 1000)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertContains(self.client.get(reverse('orders:list')), f'#{order.pk}')

    def test_checkout_requires_login(self):
        resp = self.client.get(reverse('orders:checkout'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp['Location'])

    def test_cannot_exceed_stock(self):
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 99})
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 5)

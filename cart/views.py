from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .cart import Cart


def cart_detail(request):
    return render(request, 'cart/detail.html')


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    if not product.in_stock:
        messages.error(request, f'{product.name} is out of stock.')
        return redirect(product)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
    cart = Cart(request)
    cart.add(product, quantity=max(quantity, 1), override=request.POST.get('override') == '1')
    messages.success(request, f'{product.name} is in your cart.')
    if request.POST.get('next') == 'cart':
        return redirect('cart:detail')
    return redirect(request.POST.get('back') or 'cart:detail')


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    messages.info(request, f'{product.name} was removed from your cart.')
    return redirect('cart:detail')

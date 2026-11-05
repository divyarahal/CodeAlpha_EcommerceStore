from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import OrderForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, 'Your cart is empty.')
        return redirect('products:list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            items = list(cart)
            for item in items:
                if item['quantity'] > item['product'].stock:
                    messages.error(request, f"Only {item['product'].stock} of {item['product'].name} left. Update your cart.")
                    return redirect('cart:detail')
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in items:
                    OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'], quantity=item['quantity'])
                    product = item['product']
                    product.stock -= item['quantity']
                    product.save(update_fields=['stock'])
            cart.clear()
            return redirect('orders:success', pk=order.pk)
    else:
        form = OrderForm(initial={
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
        })
    return render(request, 'orders/checkout.html', {'form': form})


@login_required
def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/success.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

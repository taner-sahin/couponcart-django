from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from cart.models import CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return redirect("cart:cart_detail")

    order = Order.objects.create(user=request.user, total_price=0)

    total_price = 0

    for item in cart_items:
        line_total = item.get_total_price()

        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_price=item.product.price,
            quantity=item.quantity,
        )

        total_price += line_total

    order.total_price = total_price
    order.save()

    cart_items.delete()

    return redirect("orders:success", order_id=order.id)

@login_required
def success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "orders/success.html", {
        "order": order
    })
    
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })
    
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "orders/order_detail.html", {
        "order": order
    })
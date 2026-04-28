from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from coupons.forms import CouponApplyForm
from products.models import Product
from .models import CartItem
from coupons.models import Coupon


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Ürün sepete eklendi.")

    return redirect("products:product_detail", slug=product.slug)


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total_price = 0

    for item in cart_items:
        total_price += item.get_total_price()

    coupon_form = CouponApplyForm()

    coupon = None
    discount_amount = 0
    final_total = total_price

    coupon_id = request.session.get("coupon_id")

    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id, active=True)
            discount_amount = total_price * coupon.discount_percent / 100
            final_total = total_price - discount_amount
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "coupon_form": coupon_form,
        "coupon": coupon,
        "discount_amount": discount_amount,
        "final_total": final_total,
    }

    return render(request, "cart/detail.html", context)

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart:cart_detail")


@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart:cart_detail")


@login_required
def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("cart:cart_detail")
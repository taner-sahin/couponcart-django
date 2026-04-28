from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def apply_coupon(request):
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data["code"]

        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            request.session["coupon_id"] = coupon.id
            messages.success(request, "Coupon applied successfully.")

        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
            messages.error(request, "Invalid coupon code.")

    return redirect("cart:cart_detail")
from django.shortcuts import render, get_object_or_404
from products.models import Product, Category



def home(request):
    products = Product.objects.filter(available=True)[:12]

    context = {
        "products": products,
    }
    return render(request, "home.html", context)



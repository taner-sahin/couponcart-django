from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(
        category=category,
        available=True
    )

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "products/category.html", context)
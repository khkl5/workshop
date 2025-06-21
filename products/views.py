from django.shortcuts import render
from .models import Product  # لو عندك موديل اسمه Product

def home_view(request):
    products = Product.objects.all()  # تجيب كل المنتجات
    return render(request, 'home.html', {'products': products})

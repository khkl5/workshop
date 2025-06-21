from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# استيراد الموديل Product
from products.models import Product

# دالة عرض الصفحة الرئيسية
def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

urlpatterns = [
    path('admin/', admin.site.urls),

    # روابط التطبيقات
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),

    # مسار الصفحة الرئيسية
    path('', home_view, name='home'),
]

# روابط الصور (لـ ImageField)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

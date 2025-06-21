from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المنتج")
    description = models.TextField(blank=True, verbose_name="وصف المنتج")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة المنتج")
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"

from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="العميل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    is_paid = models.BooleanField(default=False, verbose_name="تم الدفع؟")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="المبلغ الإجمالي")

    def __str__(self):
        return f"طلب رقم {self.id} - {self.total_amount} ريال"

    def update_total(self):
        total = sum(item.subtotal() for item in self.items.all())
        self.total_amount = total
        self.save()

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر الوحدة")

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    def subtotal(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "عنصر طلب"
        verbose_name_plural = "عناصر الطلب"
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        verbose_name = "عنصر السلة"
        verbose_name_plural = "عناصر السلة"


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="الحساب")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="رقم الجوال")
    address = models.TextField(blank=True, verbose_name="العنوان")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "الملف الشخصي"
        verbose_name_plural = "الملفات الشخصية"

# === إشارة إنشاء أو تحديث الملف الشخصي عند حفظ المستخدم ===
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

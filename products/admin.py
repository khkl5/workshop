from django.contrib import admin
from .models import Product
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at', 'image_tag')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px;" />', obj.image.url)
        return '-'
    image_tag.short_description = 'صورة'

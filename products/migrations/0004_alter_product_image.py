# Generated by Django 5.2.3 on 2025-06-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='صورة المنتج'),
        ),
    ]

from django.urls import path
from .views import (
    cart_view, 
    checkout, 
    order_success, 
    add_to_cart, 
    update_cart_item, 
    increase_cart_item, 
    decrease_cart_item
)

urlpatterns = [
    path('cart/', cart_view, name='cart'),  # صفحة السلة
    path('cart/checkout/', checkout, name='checkout'),  # إتمام الطلب
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # اضف للسلة
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/increase/<int:item_id>/', increase_cart_item, name='increase_cart_item'),
    path('cart/decrease/<int:item_id>/', decrease_cart_item, name='decrease_cart_item'),
]

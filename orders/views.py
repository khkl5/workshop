from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, CartItem
from products.models import Product
from decimal import Decimal

# عرض السلة
def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    total = sum(item.subtotal() for item in cart_items)
    tax = total * Decimal('0.15')
    grand_total = total + tax

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    })

# أضف للسلة
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product,
            defaults={'quantity': 1}
        )
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key, product=product,
            defaults={'quantity': 1}
        )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

# زيادة الكمية
def increase_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')

# إنقاص الكمية
def decrease_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity -= 1
    if item.quantity > 0:
        item.save()
    else:
        item.delete()
    return redirect('cart')

# تحديث الكمية (لو تبغين input)
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
        else:
            item.delete()

    return redirect('cart')

# إتمام الطلب
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        is_paid=False,
        total_amount=0
    )

    total = 0

    for item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        total += order_item.subtotal()

    order.total_amount = total
    order.save()

    cart_items.delete()

    return redirect('order_success', order_id=order.id)

# صفحة النجاح
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})

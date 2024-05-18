from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request, coupon_code=None):

    cart_items = []
    total = 0
    product_count = 0
    shipping_count = 0
    discount = request.session.get('coupon_discount', 0)
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            shipping_count += product.shipping
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'shipping_count': shipping_count,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                shipping_count += product.shipping
                cart_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = shipping_count
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        if delivery == 0:
            delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    grand_total = delivery + total
    
    if discount > 0:
        
        discount = total * (Decimal (discount) / 100)
        total -= discount
        grand_total -= discount
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'coupon_code': coupon_code,
        'discount': discount,
    }

    return context
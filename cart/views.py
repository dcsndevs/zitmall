from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from products.models import Product
from .models import Coupon
from cart.contexts import cart_contents



def view_cart(request):
    """ A view that renders the cart contents page """
    
    return render(request, 'cart/cart.html')

def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    coupon_code = coupon_code.upper()
    try:
        print(f"Coupon code gotten is {coupon_code}")
        coupon = Coupon.objects.get(code=coupon_code)
        today = timezone.now().date()
        if coupon.active and coupon.usage_limit > 0 and coupon.valid_from <= today <= coupon.valid_to:
            request.session['coupon_id'] = coupon.id
            request.session['coupon_discount'] = coupon.discount
            messages.success(request, f'Coupon Code: {coupon_code} has just saved you {coupon.discount}%')
            coupon.usage_limit -= 1
            coupon.used += 1
            if coupon.usage_limit == 0:
                coupon.active = False
            coupon.save()
        else:
            messages.success(request, f'This coupon code no longer active or has been used')
            # Coupon is not valid or active
            # You can handle this case as needed, such as displaying an error message
            pass
    except Coupon.DoesNotExist:
        messages.success(request, f'The entered coupon code does not exist')
        # Coupon does not exist
        # You can handle this case as needed, such as displaying an error message
        pass

    # Redirect back to the cart page after applying the coupon
    return redirect('view_cart')

def add_to_cart(request, item_id):
    """ Add a quantity of the specified product to the shopping cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})

    if size:
        if item_id in list(cart.keys()):
            if size in cart[item_id]['items_by_size'].keys():
                cart[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.title} quantity to {cart[item_id]["items_by_size"][size]}')
            else:
                cart[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.title} to your cart')
        else:
            cart[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.title} to your cart')
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(request, f'Updated {product.title} quantity to {cart[item_id]}')
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {product.title} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)
    

def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.title} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.title} from your cart')
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f'Updated {product.title} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.title} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.title} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.title} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from products.models import Product
from .models import Coupon
from cart.contexts import cart_contents
from django.http import JsonResponse
import json



def view_cart(request):
    """ A view that renders the cart contents page """
    cart = request.session.get('cart', {})
    current_cart = cart_contents(request)
    total = current_cart['discount']
    print(f'this is the {total}')
    
    return render(request, 'cart/cart.html')

def apply_coupon(request):
    if 'coupon_code' in request.session:
        messages.info(request, f'You have already applied a coupon code to this cart.'
                         ' Coupon codes can only be used per order. Thank you.')
        return redirect('view_cart')
        
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
            messages.info(request, f'This coupon code is no longer active.')
            # Coupon is not valid or active
            # You can handle this case as needed, such as displaying an error message
            pass
    except Coupon.DoesNotExist:
        messages.error(request, f'This coupon code does not exist')
        # Coupon does not exist
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
    return redirect(reverse('view_cart'))
    

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


def quick_add_to_cart(request, item_id):
    """ Add a single quantity of the specified product to the shopping cart """

    # Get the product instance
    product = get_object_or_404(Product, pk=item_id)
    
    # Set the default quantity to one
    quantity = 1
    
    # Get the redirect URL
    redirect_url = request.GET.get('redirect_url', '/')

    # Get the session cart
    cart = request.session.get('cart', {})

    # Check if the product is already in the cart
    if item_id in cart:
        # Increment the quantity by one
        cart[item_id] += quantity
        message = f'Updated {product.title} quantity to {cart[item_id]}'
    else:
        # Add the product to the cart with quantity one
        cart[item_id] = quantity
        message = f'Added {product.title} to your cart'

    # Update the session cart
    request.session['cart'] = cart
    
    return JsonResponse({'message': message})


def empty_cart(request):
    # Get the cart from the session
    cart = request.session.get('cart', {})
    
    # Clear the cart
    cart.clear()
    
    # Update the session with the empty cart
    request.session['cart'] = cart
    
    return redirect(reverse('view_cart'))    
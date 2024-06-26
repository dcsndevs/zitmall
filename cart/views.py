from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from products.models import Product
from .models import Coupon
from cart.contexts import cart_contents


def view_cart(request):
    """A view that renders the cart contents page"""
    cart = request.session.get("cart", {})
    current_cart = cart_contents(request)
    total = current_cart["discount"]

    return render(request, "cart/cart.html")


def apply_coupon(request):
    if "coupon_code" in request.session:
        messages.info(
            request,
            f"You have already applied a coupon code to this cart."
            " Coupon codes can only be used per order. Thank you.",
        )
        return redirect("view_cart")

    coupon_code = request.POST.get("coupon_code")
    coupon_code = coupon_code.upper()
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        today = timezone.now().date()
        if (
            coupon.active
            and coupon.usage_limit > 0
            and coupon.valid_from <= today <= coupon.valid_to
        ):
            request.session["coupon_id"] = coupon.id
            request.session["coupon_discount"] = coupon.discount
            messages.success(
                request,
                f"Coupon Code: {coupon_code} has just saved you"
                "{coupon.discount}%",)
            coupon.usage_limit -= 1
            coupon.used += 1
            if coupon.usage_limit == 0:
                coupon.active = False
            coupon.save()
        else:
            messages.info(request,
                          f"This coupon code is no longer active.")
            # Coupon is not valid or active
            # You can handle this case as needed,
            # such as displaying an error message
            pass
    except Coupon.DoesNotExist:
        messages.error(request, f"This coupon code does not exist")
        # Coupon does not exist
        pass

    # Redirect back to the cart page after applying the coupon
    return redirect("view_cart")


def add_to_cart(request, item_id):
    """Add a quantity of the specified product to the shopping cart"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    size = None
    if "product_size" in request.POST:
        size = request.POST["product_size"]
    cart = request.session.get("cart", {})

    # Check stock availability before adding to cart
    if not check_stock_availability(product, size, quantity, cart):
        messages.error(
            request,
            f"Sorry, you cannot add more items."
            "The maximum available stock is ${product.quantity}.",
        )
        return redirect(redirect_url)

    if size:
        if item_id in list(cart.keys()):
            if size in cart[item_id]["items_by_size"].keys():
                cart[item_id]["items_by_size"][size] += quantity
                messages.success(
                    request,
                    f'Updated size {size.upper()} {product.title}'
                    'quantity to {cart[item_id]["items_by_size"][size]}',)
            else:
                cart[item_id]["items_by_size"][size] = quantity
                messages.success(
                    request, f"Added size {size.upper()}"
                    " {product.title} to your cart"
                )
        else:
            cart[item_id] = {"items_by_size": {size: quantity}}
            messages.success(
                request, f"Added size {size.upper()}"
                " {product.title} to your cart"
            )
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(
                request, f"Updated {product.title} quantity to {cart[item_id]}"
            )
        else:
            cart[item_id] = quantity
            messages.success(request, f"Added {product.title} to your cart")

    request.session["cart"] = cart
    return redirect(reverse("view_cart"))


def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    size = None
    if "product_size" in request.POST:
        size = request.POST["product_size"]
    cart = request.session.get("cart", {})

    # Check stock availability before adding to cart
    if not check_stock_availability(product, size, quantity, cart):
        messages.error(
            request,
            f"Sorry, you cannot add more items."
            " The maximum available stock has been reached.",
        )
        return redirect(reverse("view_cart"))

    if size:
        if quantity > 0:
            cart[item_id]["items_by_size"][size] = quantity
            messages.success(
                request,
                f'Updated size {size.upper()} {product.title} quantity'
                ' to {cart[item_id]["items_by_size"][size]}',
            )
        else:
            del cart[item_id]["items_by_size"][size]
            if not cart[item_id]["items_by_size"]:
                cart.pop(item_id)
            messages.success(
                request, f"Removed size {size.upper()}"
                " {product.title} from your cart"
            )
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(
                request, f"Updated {product.title} quantity to {cart[item_id]}"
            )
        else:
            cart.pop(item_id)
            messages.success(request, f"Removed {product.title}"
                             " from your cart")

    request.session["cart"] = cart
    return redirect(reverse("view_cart"))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if "product_size" in request.POST:
            size = request.POST["product_size"]
        cart = request.session.get("cart", {})

        if size:
            del cart[item_id]["items_by_size"][size]
            if not cart[item_id]["items_by_size"]:
                cart.pop(item_id)
            messages.success(
                request, f"Removed size {size.upper()}"
                " {product.title} from your cart"
            )
        else:
            cart.pop(item_id)
            messages.success(request,
                             f"Removed {product.title} from your cart")

        request.session["cart"] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)

@csrf_exempt
def quick_add_to_cart(request, item_id):
    """Add a single quantity of the specified product to the shopping cart"""

    # Get the product instance
    product = get_object_or_404(Product, pk=item_id)

    # Set the default quantity to one
    quantity = 1

    # Get the redirect URL
    redirect_url = request.GET.get("redirect_url", "/")

    # Get the session cart
    cart = request.session.get("cart", {})

    # Check the current quantity in the cart
    current_quantity_in_cart = cart.get(item_id, 0)

    # Check if adding one more exceeds the available stock
    if current_quantity_in_cart + quantity > product.quantity:
        message = f"Sorry, {product.title} is out of stock."
        return JsonResponse({"message": message, "status": "error"})

    # Check if the product is already in the cart
    if item_id in cart:
        # Increment the quantity by one
        cart[item_id] += quantity
        message = f"Updated {product.title} quantity to {cart[item_id]}"
    else:
        # Add the product to the cart with quantity one
        cart[item_id] = quantity
        message = f"Added {product.title} to your cart"

    # Update the session cart
    request.session["cart"] = cart

    return JsonResponse({"message": message, "status": "success"})


def empty_cart(request):
    # Get the cart from the session
    cart = request.session.get("cart", {})

    # Clear the cart
    cart.clear()

    # Update the session with the empty cart
    request.session["cart"] = cart

    return redirect(reverse("view_cart"))


def check_stock_availability(product, size, quantity, cart):
    """
    Check if the requested quantity of the product is available.
    """
    available_stock = product.quantity

    if size:
        # Adjust available stock if size-based inventory is used
        if product.has_sizes:
            size_stock = product.sizes.get(size=size)
            if size_stock:
                available_stock = size_stock.quantity
            else:
                return False

    current_quantity = 0
    if product.pk in cart:
        if size:
            current_quantity = cart[product.pk]["items_by_size"].get(size, 0)
        else:
            current_quantity = cart[product.pk]

    return (current_quantity + quantity) <= available_stock

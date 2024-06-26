from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.db.models import F

from .forms import OrderForm
from vendor.models import VendorOrder
from .models import Order, OrderLineItem
from products.models import Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from cart.contexts import cart_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "cart": json.dumps(request.session.get("cart", {})),
                "save_info": request.POST.get("save_info"),
                "create_info": request.POST.get("create_info"),
                "username": request.user,
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be \
            processed right now. Please try again later.",
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        cart = request.session.get("cart", {})
        discount = request.session.get("coupon_discount", 0)

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "county": request.POST["county"],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            current_cart = cart_contents(request)
            order.discount = current_cart["discount"]
            order.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()

                        # Update product stock in database
                        Product.objects.filter(id=product.id).update(
                            quantity=F("quantity") - item_data
                        )
                        # create vendor line item
                        vendor_order_line_item = VendorOrder(
                            item=order_line_item,
                        )
                        vendor_order_line_item.save()
                    else:
                        for size, quantity in item_data[
                            "items_by_size"
                            ].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()

                            # Update product stock in database
                            Product.objects.filter(id=product.id).update(
                                quantity=F("quantity") - item_data
                            )
                            # create vendor line item
                            vendor_order_line_item = VendorOrder(
                                item=order_line_item,
                            )
                            vendor_order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        ("One of the products in your cart wasn't"
                            " found in our database. "
                            " Please call us for assistance!"),
                    )
                    order.delete()
                    return redirect(reverse("view_cart"))

            request.session["save_info"] = "save-info" in request.POST
            request.session["create_info"] = "create-info" in request.POST
            return redirect(reverse("checkout_success",
                            args=[order.order_number]))
        else:
            messages.error(
                request,
                "There was an error with your form. \
                Please double check your information.",
            )
    else:
        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request,
                           "There's nothing in your cart at the moment")
            return redirect(reverse("products"))

        current_cart = cart_contents(request)
        total = current_cart["grand_total"]
        if total > 999999.99:
            messages.error(
                request,
                "You have exceeded the order limit."
                " You cannot order upto USD 1 million at once. "
                "Kindly reduce your order items",
            )
            return redirect(reverse("view_cart"))
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(
                    initial={
                        "full_name": profile.user.get_full_name(),
                        "email": profile.user.email,
                        "phone_number": profile.default_phone_number,
                        "country": profile.default_country,
                        "postcode": profile.default_postcode,
                        "town_or_city": profile.default_town_or_city,
                        "street_address1": profile.default_street_address1,
                        "street_address2": profile.default_street_address2,
                        "county": profile.default_county,
                    }
                )
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. \
            Did you forget to set it in your environment?",
        )

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get("save_info")
    create_info = request.session.get("create_info")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                "default_phone_number": order.phone_number,
                "default_country": order.country,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
    if create_info:
        user_email = order.email
        if not User.objects.filter(email=user_email).exists():
            full_name = order.full_name.strip()
            name_parts = full_name.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            random_password = get_random_string(length=7)

            newuser = User.objects.create_user(
                username=user_email,
                email=user_email,
                first_name=first_name,
                last_name=last_name,
                password=random_password,
            )
            newuser.is_staff = False
            newuser.save()
            subject = f"Hey {order.full_name}: your Zitmall user login details"
            body = render_to_string(
                "checkout/confirmation_emails/newuser_email_body.txt",
                {
                    "order": order,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                    "random_password": random_password,
                },
            )

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])

            user_profile, created = UserProfile.objects.get_or_create(user=newuser)

            user_profile.default_phone_number = order.phone_number
            user_profile.default_country = order.country
            user_profile.default_postcode = order.postcode
            user_profile.default_town_or_city = order.town_or_city
            user_profile.default_street_address1 = order.street_address1
            user_profile.default_street_address2 = order.street_address2
            user_profile.default_county = order.county
            user_profile.save()

            order.user_profile = user_profile
            order.save()

        elif User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            user_profile = UserProfile.objects.get(user=user)
            order.user_profile = user_profile
            order.save()

    messages.success(
        request,
        f"Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.",
    )

    if "cart" in request.session:
        del request.session["cart"]

    if "coupon_discount" in request.session:
        del request.session["coupon_discount"]
        del request.session["coupon_id"]

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
    }

    return render(request, template, context)

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .forms import VendorRegistrationForm

from products.models import Product, Category


def index(request):
    """A view to return the index page"""

    products = Product.objects.all().order_by("?")[:12]
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("title"))
            if sortkey == "category":
                sortkey = "category__name"
            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(title__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
    }

    return render(request, "home/index.html", context)


def privacy_policy(request):

    return render(request, "home/privacy-policy.html")


def vendor_signup(request):

    text = "Your registration is completed!"
    " We would get back to you within 2 business working days."
    vendor_form = VendorRegistrationForm()

    if request.method == "POST":
        vendor_form = VendorRegistrationForm(request.POST)

        if vendor_form.is_valid():
            vendor_form.save()
            messages.add_message(request, messages.SUCCESS, text)
            return redirect("home")

    else:
        vendor_form = VendorRegistrationForm()
    return render(
        request,
        "home/register.html",
        {
            "vendor_form": vendor_form,
        },
    )

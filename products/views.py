from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category

# Create your views here.


def all_products(request):
    """A view to show all products, including sorting and search queries"""

    products = Product.objects.all().exclude(status=0)
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

            queries = (
                Q(title__icontains=query) 
                | Q(description__icontains=query)
            )
            products = products.filter(queries)
            
            current_sorting = f"{sort}_{direction}"
            context = {
                "search": products,
                "search_term": query,
                "current_categories": categories,
                "current_sorting": current_sorting,
            }

            return render(request, "products/products_search.html", context)

    current_sorting = f"{sort}_{direction}"

    # Pagination logic
    paginator = Paginator(products, 20)  # Show 20 products per page.
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_detail.html", context)


def product_detail_by_slug(request, product_slug):
    """A view to show individual product details"""

    product = get_object_or_404(Product, slug=product_slug)
    similar_products = (
        Product.objects.filter(category_id=product.category)
        .exclude(status=0)
        .order_by("?")[:4]
    )

    if product.status == 0:
        messages.info(request, "That product is currently unavailable.")
        return redirect("products")

    context = {
        "product": product,
        "similar_products": similar_products,
    }

    return render(request, "products/product_detail.html", context)

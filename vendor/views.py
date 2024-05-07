from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.http import JsonResponse
from .models import VendorOrder
from .forms import VendorOrderForm
from products.models import Product, Category
from products.forms import ProductForm
from checkout.models import Order, OrderLineItem

# Create your views here.
def authentication(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
def vendor_admin(request):
    
    return render(request, 'vendor/admin.html')

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.filter(vendor=request.user)
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('title'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(title__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'vendor/all-products.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.slug = slugify(product.title)
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('vendor_products'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'vendor/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    authentication(request)

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.title}')

    template = 'vendor/edit_products.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('vendor_products'))


@login_required
def vendor_orders(request):
    """ A view to show all vendor orders, including sorting and search queries """

    orders = OrderLineItem.objects.filter(product__vendor=request.user)

    context = {
        'orders': orders,
    }

    return render(request, 'vendor/orders.html', context)


def status_products(request, product_id, product_status):
    products = get_object_or_404(Product, pk=product_id)
    if products.status == 1:
        products.status = 0
        products.save()
        status = 0
        message = 'Product status updated to Draft.'
    elif products.status == 0:
        products.status = 1
        products.save()
        status = 1
        message = 'Product status updated to Published.'
    return JsonResponse({'status': status, 'message': message})


def vendor_order_view(request, order_no, orderline_id):
    order_line_item = get_object_or_404(OrderLineItem, order__order_number=order_no, id=orderline_id)
    vendor_order, created = VendorOrder.objects.get_or_create(item=order_line_item)

    if request.method == 'POST':
        form = VendorOrderForm(request.POST, instance=vendor_order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor order has been saved successfully.')
            return redirect('vendor_orders')  # Replace 'vendor_orders' with the URL name of your vendor orders list page
    else:
        form = VendorOrderForm(instance=vendor_order, disable_item_edit=not created)
    
    context = {
        'order': order_line_item,
        'form': form
    }
    
    return render(request, 'vendor/order_view.html', context)

def accept_order(request, item_id):
    """ Vendor decision to accept new orders """
    
    authentication(request)
    
    vendor_order_item = get_object_or_404(VendorOrder, pk=item_id)
    if vendor_order_item.accept == 0:
        vendor_order_item.accept = 1
        vendor_order_item.save()
        messages.success(request, 'Order fulfillment accepted! Please prepare shipment immediately.')
        return redirect('vendor_orders')
    else:
        messages.error(request, 'Failed to accept order. Kindly refresh the page.')
    
    context = {
        'vendor_order_item': vendor_order_item,
    }

    return render(request, 'vendor/orders.html', context)

def reject_order(request, item_id):
    """ Vendor decision to reject orders """
    
    authentication(request)
    
    vendor_order_item = get_object_or_404(VendorOrder, pk=item_id)
    
    if vendor_order_item.accept == 0:
        vendor_order_item.accept = 2
        vendor_order_item.save()
        messages.success(request, 'Your have rejected this Order{vendor_order_item.accept}. And it the Order canceled!')
        return redirect('vendor_orders')
    else:
        messages.error(request, 'Failed to reject order. Order is currently {vendor_order_item.accept}'
                       'Kindly refresh the page.')
        
    
    context = {
        'vendor_order_item': vendor_order_item,
    }

    return redirect('vendor_orders')


from functools import wraps
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.http import JsonResponse
from .models import VendorOrder, VendorOrderStatusHistory
from .forms import VendorOrderForm
from products.models import Product, Category
from products.forms import ProductForm
from checkout.models import Order, OrderLineItem


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Sorry, only store owners can do that.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def vendor_admin(request):
    
    return render(request, 'vendor/admin.html')

@staff_required
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


@staff_required
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


@staff_required
def edit_product(request, product_id):
    """ Edit a product in the store """

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


@staff_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('vendor_products'))


@staff_required
def vendor_orders(request):
    """ A view to show all vendor orders, including sorting and search queries """
    orders = OrderLineItem.objects.filter(product__vendor=request.user).exclude(status=0)
    orders = orders.order_by('-id')
    
    context = {
        'orders': orders,
        
    }

    return render(request, 'vendor/orders.html', context)


@staff_required
def new_vendor_orders(request):
    """ A view to show all vendor orders """

    # orders = OrderLineItem.objects.filter(product__vendor=request.user, status=0).order_by('-id')
    orders = VendorOrder.objects.filter(item__product__vendor=request.user, accept=0).order_by('-id')
    if orders.count() == 0:
        messages.info(request, f'There are no New orders.'
            ' You have been redirected to Active Order page.')
        return redirect(reverse('active_vendor_orders'))
         
    
    context = {
        'orders': orders,
    }

    return render(request, 'vendor/new_order.html', context)


#Publish product or set as draft
@staff_required
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


@staff_required
def vendor_order_view(request, order_no, orderline_id):
    order_line_item = get_object_or_404(OrderLineItem, order__order_number=order_no, id=orderline_id)
    vendor_order, created = VendorOrder.objects.get_or_create(item=order_line_item)

    condition_value = vendor_order.status
    if request.method == 'POST':
        form = VendorOrderForm(request.POST, instance=vendor_order)
        if form.is_valid():
            form.save()
            order_line_item = get_object_or_404(OrderLineItem, id=orderline_id)
            if vendor_order.reason > 0:
                messages.success(request, 'Thank you for providing a reason.')
                return redirect('vendor_orders')
            elif vendor_order.status == 0:
                order_line_item.status = 1
                order_line_item.save()
            elif vendor_order.status == 1:
                order_line_item.status = 2
                order_line_item.save()
            elif vendor_order.status == 2:
                order_line_item.status = 3
                order_line_item.save()
            elif vendor_order.status == 3:
                order_line_item.status = 4
                order_line_item.save()
            elif vendor_order.status == 4:
                order_line_item.status = 5
                order_line_item.save()
            messages.success(request, 'Order status has been updated successfully!')
            return redirect('vendor_orders')         
        
    else:
        form = VendorOrderForm(instance=vendor_order)
        
    # Retrieve the history
    history_entries = VendorOrderStatusHistory.objects.filter(vendor_order=vendor_order).order_by('-created_on')

    context = {
        'order': order_line_item,
        'form': form,
        'condition_value': condition_value,
        'history_entries': history_entries,  # Add history entries to context
    }
    
    return render(request, 'vendor/view_order_details.html', context)


@staff_required
# Vendors accept orders thereby processing it
def accept_order(request, order_number, product_id):
    """ Vendor decision to accept new orders """
    
    vendor_order_item = get_object_or_404(
        VendorOrder, 
        item__order__order_number=order_number, 
        item__product__id=product_id
        )

    if vendor_order_item.accept == 0:
        vendor_order_item.accept = 1
        vendor_order_item.save()

        order_line_item = get_object_or_404(
        OrderLineItem, 
        order__order_number=order_number, 
        product__id=product_id
        )
        order_line_item.status = 1
        order_line_item.save()
        messages.success(request, 'Order fulfillment accepted!'
                        ' Please prepare shipment immediately.')
        return redirect('new_vendor_orders')
    else:
        messages.error(request, 'Failed to accept order.'
                       'Kindly refresh the page.')
        
    context = {
        'vendor_order_item': vendor_order_item,
    }
    return render(request, 'vendor/orders.html', context)


@staff_required
# Vendors reject order thereby cancelling it
def reject_order(request, order_number, product_id):
    """ Vendor decision to reject orders """
        
    vendor_order_item = get_object_or_404(
            VendorOrder, 
            item__order__order_number=order_number, 
            item__product__id=product_id
            )

    if vendor_order_item.accept == 0:
        vendor_order_item.accept = 2
        vendor_order_item.save()

        order_line_item = get_object_or_404(
        OrderLineItem, 
        order__order_number=order_number, 
        product__id=product_id
        )
        order_line_item.status = 5
        order_line_item.save()
        messages.success(request, 'Your have rejected this Order'
                        ' and it has been marked as cancelled!')
        return redirect('new_vendor_orders')
    else:
        messages.error(request, f'Failed to reject order.'
                       ' Kindly refresh the page.')
        
    context = {
        'vendor_order_item': vendor_order_item,
    }

    return render(request, 'vendor/orders.html', context)


# Wether Vendor wants to ship item themselve or not
@staff_required
def shipment_type(request, order_number, product_id):

    vendor_order_item = get_object_or_404(
        VendorOrder, 
        item__order__order_number=order_number, 
        item__product__id=product_id
        )
    
    if vendor_order_item.fulfilment == 2:
        vendor_order_item.fulfilment = 1
        vendor_order_item.save()
        product_status = 1
        message = 'Shipment type has been set to self. You still have to accept the order in other to begin shipment process.'
    
    elif vendor_order_item.fulfilment == 1:
        vendor_order_item.fulfilment = 2
        vendor_order_item.save()
        product_status = 2
        message = 'Shipment type has been set to Zit-Ship. Kindly accept the order and prepare the order for pickup from Zit Ship Team.'
    
    elif vendor_order_item.fulfilment == 0:
        message = 'This Order has since been cancelled. You can no longer ship. Contact Support for help.'    
    
    return JsonResponse({'product_status': product_status, 'message': message})

@staff_required
def cancelled_vendor_orders(request):
    """ A view to show all canclled vendor orders"""

    orders = OrderLineItem.objects.filter(product__vendor=request.user, status=5).order_by('-id')
    
    context = {
        'orders': orders,
    }

    return render(request, 'vendor/cancelled_orders.html', context)


@staff_required
def active_vendor_orders(request):
    """ A view to show all cancelled vendor orders"""
    
    orders = OrderLineItem.objects.filter(
    product__vendor=request.user,
    status__in=[1, 2])
    
    if orders.count() == 0:
        messages.info(request, f'There are no Active orders.'
                    ' You have been redirected to All Order page history')
        return redirect(reverse('vendor_orders'))
    
    context = {
        'orders': orders,
    }

    return render(request, 'vendor/active_orders.html', context)


@staff_required
# Vendors cancel order
def cancel_order(request, order_number, product_id):
    """ Vendor decision to cancel orders """
    reason_value = request.POST.get('cancel_reason')
    vendor_order_item = get_object_or_404(
            VendorOrder, 
            item__order__order_number=order_number, 
            item__product__id=product_id
            )

    order_line_item = get_object_or_404(
        OrderLineItem, 
        order__order_number=order_number, 
        product__id=product_id
        )
    if vendor_order_item.accept == 0:
        messages.error(request, 'You are yet to accept/reject this shipment.'
                       ' You can only cancel orders that you have accepted.'
                       ' Go to the new orders pageto reject it!')
    else:
        vendor_order_item.status = 4
        vendor_order_item.reason = reason_value
        vendor_order_item.save()
        
        order_line_item.status = 5
        order_line_item.save()

    if vendor_order_item.status == 4:
            messages.success(request, 'Your have set the order as canceled')
            return redirect('vendor_order_view', order_no=order_number, orderline_id=order_line_item.id)

    return redirect('vendor_order_view', order_no=order_number, orderline_id=order_line_item.id)



@staff_required
# Vendors ship order
def ship_order(request, order_number, product_id):
    """ Vendor decision to cancel orders """
    
    vendor_order_item = get_object_or_404(
            VendorOrder, 
            item__order__order_number=order_number, 
            item__product__id=product_id
            )
    
    order_line_item = get_object_or_404(
        OrderLineItem, 
        order__order_number=order_number, 
        product__id=product_id
        )
    
    if vendor_order_item.accept == 0:
        messages.error(request, "You are yet to accept this shipment. Go to the new order sction and accept it first!")
    else:
        vendor_order_item.status = 1
        vendor_order_item.save()

        order_line_item.status = 2
        order_line_item.save()
    
    if vendor_order_item.status == 1:
            messages.success(request, 'Your have set the order as shipped!')
            return redirect('vendor_order_view', order_no=order_number, orderline_id=order_line_item.id)

    return redirect('vendor_order_view', order_no=order_number, orderline_id=order_line_item.id)


@staff_required
# Vendors deliver order
def deliver_order(request, order_number, product_id):
    """ Vendor decision to deliver orders """
    
    vendor_order_item = get_object_or_404(
            VendorOrder, 
            item__order__order_number=order_number, 
            item__product__id=product_id
            )
    
    order_line_item = get_object_or_404(
        OrderLineItem, 
        order__order_number=order_number, 
        product__id=product_id
        )
    if vendor_order_item.accept == 0:
        messages.error(request, "You are yet to accept this shipment. Go to the new order sction and accept it first!")
    else:
        vendor_order_item.status = 2
        vendor_order_item.save()

        order_line_item.status = 3
        order_line_item.save()
    
    if vendor_order_item.status == 2:
        messages.success(request, 'Your have set the order to Delivered!')
        return redirect('vendor_order_view', order_no=order_number, orderline_id=order_line_item.id)

    return render(request, 'vendor_order_view')

@staff_required
# Vendors delivery failed order
def delivery_failed_order(request, order_number, product_id):
    """ Vendor decision to fail the ongoing delivery orders """
    
    vendor_order_item = get_object_or_404(
            VendorOrder, 
            item__order__order_number=order_number, 
            item__product__id=product_id
            )
    
    order_line_item = get_object_or_404(
        OrderLineItem, 
        order__order_number=order_number, 
        product__id=product_id
        )
    
    if vendor_order_item.accept == 0:
        messages.error(request, "You are yet to accept this shipment. Go to the new order sction and accept it first!")
    else:
        vendor_order_item.status = 3
        vendor_order_item.save()

        order_line_item.status = 4
        order_line_item.save()
    
    if vendor_order_item.status == 3:
        messages.success(request, 'Your have set the order to Delivery failed!')
        return redirect('vendor_order_view', order_no=order_number, orderline_id=order_line_item.id)

    return render(request, 'vendor_order_view')


@staff_required
def delivered_vendor_orders(request):
    """ A view to show all delivered vendor orders"""

    orders = OrderLineItem.objects.filter(product__vendor=request.user, status=3).order_by('-id')
    
    context = {
        'orders': orders,
    }

    return render(request, 'vendor/delivered_orders.html', context)

@staff_required
def delivery_failed_vendor_orders(request):
    """ A view to show all delivery failed vendor orders"""

    orders = OrderLineItem.objects.filter(product__vendor=request.user, status=4).order_by('-id')
    
    context = {
        'orders': orders,
    }

    return render(request, 'vendor/delivery_failed_orders.html', context)
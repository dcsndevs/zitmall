from django.conf import settings
from vendor.models import OrderLineItem


def new_orders(request):
    neworders = 0
    context = {}
    if request.user.is_authenticated and request.user.is_staff:
        neworders = OrderLineItem.objects.filter(product__vendor=request.user, status=0).order_by('-id').count()
        context['neworders'] = neworders
    return context


def active_orders(request):
    active_orders = 0
    context = {}
    if request.user.is_authenticated and request.user.is_staff:
        active_orders = OrderLineItem.objects.filter(
    product__vendor=request.user,
    status__in=[1, 2]).count()
        
    context['active_orders'] = active_orders
    return context

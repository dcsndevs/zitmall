from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import VendorOrder, VendorOrderStatusHistory

@receiver(pre_save, sender=VendorOrder)
def create_vendor_order_status_history(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update to an existing instance
        previous = VendorOrder.objects.get(pk=instance.pk)
        changes = []

        if previous.accept != instance.accept:
            changes.append(f' Order {instance.get_accept_display()}')
        if previous.fulfilment != instance.fulfilment:
            changes.append(f' Fulfilment set to {instance.get_fulfilment_display()}')
        if previous.status != instance.status:
            changes.append(f' Order status: {instance.get_status_display()}')
        if previous.reason != instance.reason:
            current_reason = instance.get_reason_display() if instance.reason is not None else 'None'
            if current_reason == "0":
                current_reason = "Out of Stock"
            if current_reason == "1":
                current_reason = "Price Difference"
            if current_reason == "2":
                current_reason = "Customer Request"
            if current_reason == "3":
                current_reason = "Other"   
            changes.append(f"Reason: {current_reason}")

        if changes:
            VendorOrderStatusHistory.objects.create(
                vendor_order=instance,
                history=" - ".join(changes)
            )
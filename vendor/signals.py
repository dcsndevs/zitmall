from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import VendorOrder, VendorOrderStatusHistory

@receiver(pre_save, sender=VendorOrder)
def create_vendor_order_status_history(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an update to an existing instance
        previous = VendorOrder.objects.get(pk=instance.pk)
        changes = []

        if previous.accept != instance.accept:
            print('Accept jknfdishfndiuhgfruhnuj')
            changes.append(instance.get_accept_display())
        if previous.fulfilment != instance.fulfilment:
            changes.append(instance.get_fulfilment_display())
        if previous.status != instance.status:
            changes.append(instance.get_status_display())
        if previous.reason != instance.reason:
            previous_reason = previous.get_reason_display() if previous.reason is not None else 'None'
            current_reason = instance.get_reason_display() if instance.reason is not None else 'None'
            changes.append(f"Cancellation Reason: {previous_reason} -> {current_reason}")

        if changes:
            VendorOrderStatusHistory.objects.create(
                vendor_order=instance,
                history="; ".join(changes)
            )
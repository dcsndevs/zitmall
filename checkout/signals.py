from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


from .models import OrderLineItem

@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()

@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()
    

@receiver(post_save, sender=OrderLineItem)
def create_user_after_purchase(sender, instance, created, **kwargs):
    """
    Automatically create a superuser account for the user after they have successfully purchased.
    """
    if created:  # Check if a new purchase was created
        user_email = instance.order.email
        if not User.objects.filter(email=user_email).exists():
            User.objects.create_user(username=user_email, email=user_email, password=instance.order.order_number)
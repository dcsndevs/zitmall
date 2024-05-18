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
def create_superuser_after_purchase(sender, instance, created, **kwargs):
    """
    Automatically creates a user account for the user after they have successfully purchased.
    """
    if created:  # Check if a new purchase was created
        user_email = instance.user.email
        # Check if the user with this email already exists
        if not User.objects.filter(email=user_email).exists():
            # Create a superuser with the user's email and a default password
            User.objects.create_superuser(email=user_email, password=OrderLineItem.order.order_number)
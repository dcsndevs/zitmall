from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail



from .models import OrderLineItem
from profiles.models import UserProfile

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
        order = instance.order
        user_email = instance.order.email
        if not User.objects.filter(email=user_email).exists():
            full_name = instance.order.full_name.strip()
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            random_password = get_random_string(length=7)
            
            user = User.objects.create_user(
                username=user_email,
                email=user_email,
                first_name=first_name,
                last_name=last_name,
                password=instance.order.order_number
            )
            user.is_staff = False
            user.save()
            subject = f'Hey {order.full_name}: your Zitmall user login details'
            body = render_to_string(
                'checkout/confirmation_emails/newuser_email_body.txt',
                {'order': order,
                 'contact_email': settings.DEFAULT_FROM_EMAIL,
                 'random_password': random_password})
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [user_email]
            )   
            
            user_profile, created = UserProfile.objects.get_or_create(
                    user=user)

            instance.order.user_profile = user_profile
            instance.order.save()
            
            user_profile.default_phone_number = instance.order.phone_number
            user_profile.default_country = instance.order.country
            user_profile.default_postcode = instance.order.postcode
            user_profile.default_town_or_city = instance.order.town_or_city
            user_profile.default_street_address1 = instance.order.street_address1
            user_profile.default_street_address2 = instance.order.street_address2
            user_profile.default_county = instance.order.county
            user_profile.save()
            
  
            


    

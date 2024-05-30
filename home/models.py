from django.db import models
from django_countries.fields import CountryField


class VendorRegistration(models.Model):
    """
    Stores a single registration form entry for vendors.
    """
  
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    current_website = models.CharField(max_length=60, null=True, blank=True)
    store_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"New Vendor registration from {self.store_name}"
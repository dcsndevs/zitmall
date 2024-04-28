from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "draft"), (1, "published"))

class Category(models.Model):
    """
    Product category names.
    """

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Product details.
    """
    
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    product_type =  models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    
    sku = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=1000, unique=True)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    old_price = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image_2 = models.ImageField(null=True, blank=True)
    image_3 = models.ImageField(null=True, blank=True)
    product_brand = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="seller",
                               default=1, null=False)
    tag = models.CharField(max_length=254, blank=True,
                           null=True, help_text="Enter tags separated by commas")
    weight = models.DecimalField(max_digits=10, decimal_places=2,
                                 default=0, blank=True,
                                 help_text="Weight of the product in kilograms")
    slug = models.SlugField(max_length=1000, unique=True)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.title
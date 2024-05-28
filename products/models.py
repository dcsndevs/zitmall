from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))

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
    
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    product_type =  models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=1000, unique=True)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False,
                                    null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    old_price = models.DecimalField(max_digits=6, decimal_places=0,
                                    null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=0,
                                    null=True, blank=True)
    image_1= models.ImageField(null=True, blank=True,
                                      help_text="This is the first image"
                                      "that site users would see")
    image_1_alt = models.CharField(max_length=50, null=True, blank=True,
                                         help_text="Default Image alt text")
    image_2 = models.ImageField(null=True, blank=True)
    image_2_alt = models.CharField(max_length=50, null=True, blank=True,
                                   help_text="Image-2 alt text")
    image_3 = models.ImageField(null=True, blank=True)
    image_3_alt = models.CharField(max_length=50,
                                   null=True, blank=True,
                                   help_text="Image-3 alt text")
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image_url_alt = models.CharField(max_length=50, null=True, blank=True,
                                     help_text="Image url alt text")
    product_brand = models.CharField(max_length=50, null=True, blank=True)
    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="seller",
        default=1,
        null=False
    )
    tag = models.CharField(max_length=254,
                           blank=True,
                           null=True, 
                           help_text="Enter tags separated by commas")
    shipping = models.DecimalField(max_digits=6, decimal_places=0,
                                   null=True, blank=True,
                                   help_text="Shipping fee for this product")
    
    slug = models.SlugField(max_length=1000, unique=True)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == 0:  # If the status is "Draft"
            self.quantity = 0  # Set the quantity to zero
        super(Product, self).save(*args, **kwargs)
from django.db import models
from checkout.models import OrderLineItem

ACCEPT = ((0, "Pending"), (1, "Yes"), (2, "No"))
FULFILMENT = ((0, "Cancelled"), (1, "Self"), (2, "Zit Ship"))
STATUS = ((0, "Preparing to ship"), (1, "Shipped"), (2, "Delivered"), (3, "Delivery Failed"), (4, "Canceled"))
REASON = (
    (0, "Out of Stock"),
    (1, "Price Difference"),
    (2, "other")
)

class VendorOrder(models.Model):
    item = models.OneToOneField(OrderLineItem, null=False, blank=False, on_delete=models.CASCADE, related_name='vendor_order_number_item')
    accept = models.IntegerField(choices=ACCEPT, default=0)
    fulfilment = models.IntegerField(choices=FULFILMENT, default=2)
    status = models.IntegerField(choices=STATUS, default=0)
    reason = models.IntegerField(choices=REASON, null=True, blank=True)
    
    def __str__(self):
        return f"{self.item.order.order_number} | {self.item.product.sku} | {self.item.product.title}"

    def save(self, *args, **kwargs):
        # Check if accept is set to "No"
        if self.accept == 2:  # Assuming 2 corresponds to "No"
            # Set fulfilment to "Cancelled"
            self.fulfilment = 0  # Assuming 0 corresponds to "Cancelled"
            self.status = 4
        
        if self.status > 1:  # Assuming 2 corresponds to "Delivered"
            # Disable other status options
            self._meta.get_field('status').choices = ((2, "Delivered"),) 
        
        super().save(*args, **kwargs)
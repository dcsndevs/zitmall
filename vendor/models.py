from django.db import models
from checkout.models import OrderLineItem

ACCEPT = ((0, "Pending"), (1, "Accepted"), (2, "Rejected"))
FULFILMENT = ((0, "Cancelled"), (1, "Self"), (2, "Zit Ship"))
STATUS = (
    (0, "Preparing to ship"),
    (1, "Shipped"),
    (2, "Delivered"),
    (3, "Delivery Failed"),
    (4, "Cancelled"),
)
REASON = (
    (0, "Out of Stock"),
    (1, "Price Difference"),
    (2, "Customer request"),
    (3, "Other"),
)


class VendorOrder(models.Model):
    item = models.OneToOneField(
        OrderLineItem,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="vendor_order_number_item",
    )
    accept = models.IntegerField(choices=ACCEPT, default=0)
    fulfilment = models.IntegerField(choices=FULFILMENT, default=2)
    status = models.IntegerField(choices=STATUS, default=0)
    reason = models.IntegerField(choices=REASON, null=True, blank=True)

    def __str__(self):
        return f"{self.item.order.order_number} |"
        "{self.item.product.sku} | {self.item.product.title}"

    def save(self, *args, **kwargs):
        # Disables status option when acceptance is still pending
        if self.pk is not None:
            # This is an update operation
            previous = VendorOrder.objects.get(pk=self.pk)
            if previous.accept == 0 and self.accept == 0:
                self.status = previous.status

        # Check if accept is set to "No"
        if self.accept == 2:  # Assuming 2 corresponds to "No"
            # Set fulfilment to "Cancelled"
            self.fulfilment = 0  # Assuming 0 corresponds to "Cancelled"
            self.status = 5

        super().save(*args, **kwargs)


class VendorOrderStatusHistory(models.Model):
    vendor_order = models.ForeignKey(
        VendorOrder, null=False, blank=False, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set the field to now when the object is first created
    history = models.TextField()  # Store the history as a string

    def __str__(self):
        return f"{self.vendor_order} - {self.history} at {self.created_on}"

from django.db import models

class Coupon(models.Model):
    class Meta:
        verbose_name_plural = 'Coupon Codes'
        
    code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(default=0)
    valid_from = models.DateField()
    valid_to = models.DateField()
    usage_limit = models.PositiveIntegerField(default=1)
    used = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)
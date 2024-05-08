from django import forms
from .models import VendorOrder


class VendorOrderForm(forms.ModelForm):

    class Meta:
        model = VendorOrder
        fields = ['status']

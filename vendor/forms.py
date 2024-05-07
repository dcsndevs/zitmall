from django import forms
from .models import VendorOrder, OrderLineItem


class VendorOrderForm(forms.ModelForm):

    class Meta:
        model = VendorOrder
        fields = ['status']

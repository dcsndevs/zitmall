from django import forms
from .models import VendorOrder, OrderLineItem


class VendorOrderForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.disable_item_edit = kwargs.pop('disable_item_edit', False)
    #     super().__init__(*args, **kwargs)
    #     if self.disable_item_edit:
    #         self.fields['item'].disabled = True

    class Meta:
        model = VendorOrder
        fields = ['fulfilment', 'status']

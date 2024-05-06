from django import forms
from .models import VendorOrder, OrderLineItem


# class VendorOrderForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         order_line_item_id = kwargs.pop('order_line_item_id', None)  # Get the OrderLineItem ID from kwargs
#         super().__init__(*args, **kwargs)
#         if order_line_item_id:
#             # Filter the item field queryset based on the OrderLineItem ID
#             self.fields['item'].queryset = OrderLineItem.objects.filter(id=order_line_item_id)

#     class Meta:
#         model = VendorOrder
#         fields = ['item', 'accept', 'fulfilment', 'status', 'reason']
        


class VendorOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        order_line_item_id = kwargs.pop('order_line_item_id', None)
        super().__init__(*args, **kwargs)
        if order_line_item_id:
            order_line_item = OrderLineItem.objects.get(id=order_line_item_id)
            # Set the initial value of the item field
            self.initial['item'] = order_line_item

    class Meta:
        model = VendorOrder
        fields = ['item', 'accept', 'fulfilment', 'status', 'reason']

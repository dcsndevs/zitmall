# forms.py
from django import forms
from .models import VendorOrder

class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrder
        fields = ['accept', 'fulfilment', 'status', 'reason']
    
    def __init__(self, *args, **kwargs):
        condition_value = kwargs.pop('condition_value', None)
        super(VendorOrderForm, self).__init__(*args, **kwargs)
        
        if condition_value is not None and condition_value > 2:
            self.fields['status'].widget.attrs['disabled'] = 'disabled'
            self.fields['status'].disabled = True  # Ensure it's not editable in the backend

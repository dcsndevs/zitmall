from django import forms
from .models import VendorOrder


class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrder
        fields = ["accept", "fulfilment", "status", "reason"]

    def __init__(self, *args, **kwargs):

        super(VendorOrderForm, self).__init__(*args, **kwargs)

        self.fields["status"].choices = [
         choice for choice in self.fields["status"].choices if choice[0] != 4
        ]

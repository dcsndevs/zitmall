from .models import VendorRegistration
from django import forms

class VendorRegistrationForm(forms.ModelForm):
    """
    Form class for users to register as vendors
    """
    class Meta:
        model = VendorRegistration
        exclude = ('none',)



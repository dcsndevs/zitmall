from django import forms
from .models import UserProfile, UserFullnameEmail
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False


class UserFullnameEmailForm(forms.ModelForm):
    class Meta:
        model = UserFullnameEmail
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.user = kwargs.pop('user', None)
        super(UserFullnameEmailForm, self).__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True, user_id=None):
        instance = super(UserFullnameEmailForm, self).save(commit=False)
        if user_id:
            instance.owner_id = user_id
        if commit:
            instance.save()
        return instance


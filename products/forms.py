from django import forms
from django.utils.text import slugify
from django_summernote.widgets import SummernoteWidget
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['slug', 'vendor']
        widgets = {
            'description': SummernoteWidget(),
        }

    image_1 = forms.ImageField(label='Image',
                               required=False,
                               widget=CustomClearableFileInput)
    image_2 = forms.ImageField(label='Image2',
                               required=False,
                               widget=CustomClearableFileInput)
    image_3 = forms.ImageField(label='Image3',
                               required=False,
                               widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the currently logged-in user
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

        if user:
            self.instance.vendor = user
            # Set the vendor field to the currently logged-in user

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if title:
            slug = slugify(title)
            cleaned_data['slug'] = slug

        return cleaned_data

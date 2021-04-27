from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'address_1', 'address_2', 'postcode', 'city',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'address_1': 'Address 1',
            'address_2': 'Address 2',
            'postcode': 'Postal Code',
            'city': 'City',
        }

        # Set cursor to this input field upon loading
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Make city and email readonly
        self.fields['city'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field in self.fields:
            if self.fields[field].required:
                # If the current field is required, add '*'
                placeholder = f'{placeholders[field]} *'
            else:
                # Otherwise just assign it to the variable 'placeholder'
                placeholder = placeholders[field]
            # Add the placeholder value from the dictionary to the input field
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Give each field this class
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Remove the label for each field
            self.fields[field].label = False
        
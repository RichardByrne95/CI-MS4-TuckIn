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
            'city': 'City',
            'postcode': 'Postal Code',
        }

        # Set cursor to this input field upon loading
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Make city readonly
        self.fields['city'].widget.attrs['readonly'] = True

        # Field processing
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
        
        #Add regular expression to fields
        self.fields['full_name'].widget.attrs['pattern'] = "[a-zA-ZÀ-ÿ-' ]{5,50}"
        self.fields['phone_number'].widget.attrs['pattern'] = '[0-9]{7,15}'
        self.fields['address_1'].widget.attrs['pattern'] = "[a-zA-Z0-9À-ÿ-' ]{5,80}"
        self.fields['address_2'].widget.attrs['pattern'] = "[a-zA-Z0-9À-ÿ-' ]{5,80}"
        self.fields['postcode'].widget.attrs['pattern'] = '[a-zA-Z0-9 ]{7}'

        # Add onInvalid to fields
        self.fields['full_name'].widget.attrs['title'] = 'Between 5 and 50 letters'
        self.fields['phone_number'].widget.attrs['title'] = 'Between 7 and 15 digits'
        self.fields['address_1'].widget.attrs['title'] = 'Between 5 and 80 characters'
        self.fields['address_2'].widget.attrs['title'] = 'Between 5 and 80 characters'
        self.fields['postcode'].widget.attrs['title'] = 'e.g D01HR04, D01 HR04'

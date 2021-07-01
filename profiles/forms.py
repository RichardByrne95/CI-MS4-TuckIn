from django import forms
from .models import CustomerProfile


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = ('customer',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'email': 'Email',
            'full_name': 'Full Name',
            'default_phone_number': 'Phone Number',
            'default_address_1': 'Address 1',
            'default_address_2': 'Address 2',
            'default_city': 'City',
            'default_postcode': 'Postcode',
        }
        # Set cursor default field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Make city readonly
        self.fields['default_city'].widget.attrs['readonly'] = True

        for field in self.fields:
            # Add asterisks to required fields only
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # Add placeholders and classes to form, remove label
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            self.fields[field].label = False
        
        #Add regular expression to fields
        self.fields['full_name'].widget.attrs['pattern'] = '[a-zA-ZÀ-ÿ ]{5,50}'
        self.fields['default_phone_number'].widget.attrs['pattern'] = '[0-9]{7,15}'
        self.fields['default_address_1'].widget.attrs['pattern'] = '[a-zA-Z0-9À-ÿ ]{5,80}'
        self.fields['default_address_2'].widget.attrs['pattern'] = '[a-zA-Z0-9À-ÿ ]{5,80}'
        self.fields['default_postcode'].widget.attrs['pattern'] = '[a-zA-Z0-9 ]{7}'

        # Add onInvalid to fields
        self.fields['full_name'].widget.attrs['title'] = 'Between 5 and 50 letters'
        self.fields['default_phone_number'].widget.attrs['title'] = 'Between 7 and 15 digits'
        self.fields['default_address_1'].widget.attrs['title'] = 'Between 5 and 80 characters'
        self.fields['default_address_2'].widget.attrs['title'] = 'Between 5 and 80 characters'
        self.fields['default_postcode'].widget.attrs['title'] = 'e.g D01HR04, D01 HR04'

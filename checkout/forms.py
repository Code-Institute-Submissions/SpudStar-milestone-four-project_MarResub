from django import forms
from .models import Order

# The order form setup, uses three fields for the user to fill


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Sets the fields of the Order model to use
        fields = ('full_name', 'email', 'user_trainer_code')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'user_trainer_code': 'Trainer Code',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = True

from django import forms
from .models import UserProfile


# Creates a form for the user's input
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Excludes the fields the user shouldn't be able to change
        exclude = ('user', 'subscription',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        # Sets placeholder values
        placeholders = {
            'default_trainer_code': 'Trainer Code',
            'default_email': 'Email',
        }

        self.fields['default_trainer_code'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False

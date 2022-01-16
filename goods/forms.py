
from django import forms
from .models import Info, Category


# Makes the form for editing and adding a product
class ProductForm(forms.ModelForm):

    class Meta:
        model = Info
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Ensures Type 1 and 2 will always be a valid type
        self.fields['type1'].choices = friendly_names
        self.fields['type2'].choices = friendly_names

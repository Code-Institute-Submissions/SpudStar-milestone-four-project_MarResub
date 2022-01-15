
from django import forms
from .models import Info, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Info
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['type1'].choices = friendly_names
        self.fields['type2'].choices = friendly_names

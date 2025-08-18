from django import forms
from .models import Collection
from recipes.models import Recipe

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name']

from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title', 'calories', 'cuisine', 'difficulty', 'veg_type', 
            'image', 'prep_time', 'total_time', 'instructions',
        )

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'unit', 'optional')

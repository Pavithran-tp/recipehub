from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    is_chef = forms.BooleanField(
        required=False,
        label="I am a chef (can create recipes)",
        widget=forms.CheckboxInput()  
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_chef',)

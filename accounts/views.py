from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

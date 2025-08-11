from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import FormView
from .forms import CustomUserCreationForm

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

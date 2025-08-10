from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # optional: auto-login after signup
            return redirect('home')  # redirect to home or dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

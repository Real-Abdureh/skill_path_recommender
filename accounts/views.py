from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm # Used by LoginView if not overridden by a custom form
from django.contrib.auth.views import LoginView # Will be used in urls.py
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from .forms import SignUpForm, UserUpdateForm

def home(request): # Keep the existing home view
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard') # Or 'home' or wherever you want to redirect after signup
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# Using a function-based view for profile update for consistency with signup
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Your profile was successfully updated!') # Optional: Add messages
            return redirect('accounts:dashboard') # Or to a profile page
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})

# LoginView and LogoutView will be configured in urls.py
# No custom view code needed here for them if using Django's defaults with template_name.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('landing_page')

# User Dashboard View (Available to authenticated users)
@login_required
def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'auth/dashboard.html')
    return redirect('login')

# Admin Panel View (Accessible only to admins)
@login_required
def admin_panel_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, 'auth/admin_panel.html')

# Password Change View (Optional)
@login_required
def change_password_view(request):
    if request.method == 'POST':
        # Handle password change logic here
        pass  # You can use Django's built-in password change form
    return render(request, 'change_password.html')

# Password Reset View (Optional)
def password_reset_view(request):
    # Use Django's built-in password reset mechanism
    pass

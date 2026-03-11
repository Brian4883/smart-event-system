# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, UpdateProfileForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')

        else:
            print("FORM ERRORS:", form.errors)   # Debug

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == "admin":
                return redirect('admin_dashboard')

            elif user.role == "organizer":
                return redirect('organizer_dashboard')

            else:
                return redirect('attendee_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')


# -------- PASSWORD RESET FUNCTIONALITY --------
def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='users/password_reset_email.html',
                subject_template_name='users/password_reset_subject.txt',
                use_https=request.is_secure(),
            )
            messages.success(request, "Password reset email sent!")
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


@login_required
def admin_dashboard(request):

    if request.user.role != "admin":
        return HttpResponseForbidden("You are not allowed here")

    return render(request, "dashboards/admin_dashboard.html")


@login_required
def organizer_dashboard(request):
    return render(request, "dashboards/organizer_dashboard.html")


@login_required
def attendee_dashboard(request):
    return render(request, "dashboards/attendee_dashboard.html")


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def update_profile(request):

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'users/update_profile.html', {'form': form})
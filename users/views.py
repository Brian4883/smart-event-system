# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CustomUserCreationForm, UpdateProfileForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# If you have events app
from events.models import Event

User = get_user_model()


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

    total_users = User.objects.count()
    total_events = Event.objects.count()

    context = {
        "total_users": total_users,
        "total_events": total_events,
    }

    return render(request, "dashboards/admin_dashboard.html", context)

@login_required
def admin_users(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    users = User.objects.all()
    return render(request, "admin/users.html", {"users": users})


@login_required
def change_user_role(request, user_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")
        user.role = new_role
        user.save()
        messages.success(request, "User role updated successfully")

    return redirect("admin_users")


@login_required
def admin_events(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    events = Event.objects.all()
    return render(request, "admin/events.html", {"events": events})


@login_required
def generate_report(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Smart Event System Report", styles['Title']))

    total_users = User.objects.count()
    total_events = Event.objects.count()

    content.append(Paragraph(f"Total Users: {total_users}", styles['Normal']))
    content.append(Paragraph(f"Total Events: {total_events}", styles['Normal']))

    doc.build(content)

    return response


@login_required
def export_users_csv(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Role'])

    for user in User.objects.all():
        writer.writerow([user.username, user.email, user.role])

    return response


@login_required
def delete_user(request, user_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    user = User.objects.get(id=user_id)
    user.delete()

    messages.success(request, "User deleted successfully")
    return redirect("admin_users")


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

    return render(request, 'update_profile.html', {'form': form})
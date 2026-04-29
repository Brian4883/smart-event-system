# users/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CustomUserCreationForm, UpdateProfileForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from events.models import Event
from tickets.models import Ticket 
from django.utils.timezone import now
from users.models import CustomUser
from openpyxl import Workbook
from datetime import datetime
from django.utils import timezone



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

            # 🔥 BLOCK unapproved organizers
            if user.role == "organizer" and not user.is_verified:
                messages.warning(request, "Your organizer account is pending admin approval.")
                return redirect('login')

            # ✅ Login allowed users
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
        return HttpResponseForbidden()

    users = User.objects.all()
    total_users = User.objects.count()
    total_organizers = User.objects.filter(role="organizer").count()

    unverified_organizers = User.objects.filter(role="organizer", is_verified=False)

  
    context = {
        "users": users,
        "total_users": total_users,
        "total_organizers": total_organizers,
        "unverified_organizers": unverified_organizers,
     
    }

    return render(request, "dashboards/admin_dashboard.html", context)


@login_required
def admin_users(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("Unauthorized")

    users = User.objects.all()
    return render(request, "admin/users.html", {"users": users})


@login_required
def verify_organizer(request, user_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("Not allowed")

    user = get_object_or_404(User, id=user_id)

    # Only verify organizers
    if user.role == "organizer":
        user.is_verified = True
        user.save()
        messages.success(request, f"{user.username} has been verified.")

    return redirect('admin_dashboard')


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


# VIEW USER 
def view_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, "view_user.html", {"u": user})


# DEACTIVATE USER
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect("admin_dashboard")


# ACTIVATE USER
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    return redirect("admin_dashboard")


# DELETE USER
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect("admin_dashboard")


@login_required
def download_users_report(request):

    if request.user.role != "admin":
        return HttpResponse("Unauthorized", status=403)

    filename = f"users_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Users Report"

    ws.append(["Username", "Email", "Role", "Status"])

    users = CustomUser.objects.all()

    for u in users:
        if u.role == "organizer":
            status = "Approved" if u.is_verified else "Pending"
        else:
            status = "Active"

        ws.append([
            u.username,
            u.email,
            u.role,
            status
        ])

    wb.save(response)
    return response


@login_required
def download_organizer_report(request):

    if request.user.role != "organizer":
        return HttpResponse("Unauthorized", status=403)

    filename = f"my_events_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb = Workbook()
    ws = wb.active
    ws.title = "My Events"

    ws.append(["Title", "Location", "Date", "Price", "Status"])

    events = Event.objects.filter(organizer=request.user)

    for event in events:
        ws.append([
            event.title,
            getattr(event, "location", "N/A"),
            str(event.start_date),
            getattr(event, "price", 0),
            "Approved" if getattr(event, "is_approved", True) else "Pending"
        ])

    wb.save(response)
    return response


@login_required
def organizer_dashboard(request):

    now = timezone.now()

    my_events = Event.objects.filter(organizer=request.user)

    total_events = my_events.count()
    upcoming_events = my_events.filter(start_date__gte=now).count()
    past_events = my_events.filter(start_date__lt=now).count()

    context = {
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "my_events": my_events,
    }

    return render(request, "dashboards/organizer_dashboard.html", context)
    
@login_required
def attendee_dashboard(request):
    upcoming_events = Event.objects.filter(is_approved=True, start_date__gte=now()).order_by('start_date')[:6]

    tickets = Ticket.objects.filter(user=request.user) if 'Ticket' in globals() else []

    context = {
        'upcoming_events': upcoming_events,
        'tickets': tickets,
        'tickets_count': len(tickets),
        'attended_count': 0, 
    }

    return render(request, "dashboards/attendee_dashboard.html", context)

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
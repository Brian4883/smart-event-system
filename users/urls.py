# users/urls.py
from django.urls import path
from .views import register_view, login_view, logout_view, password_reset_view, admin_dashboard, organizer_dashboard, attendee_dashboard, profile, update_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('attendee-dashboard/', attendee_dashboard, name='attendee_dashboard'),


    path('password-reset/', password_reset_view, name='password_reset'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

]
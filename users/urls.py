# users/urls.py
from django.urls import path
from .views import register_view, login_view, logout_view, password_reset_view, admin_dashboard, organizer_dashboard, attendee_dashboard, profile, update_profile, admin_dashboard, admin_events, admin_users, change_user_role, export_users_csv, generate_report, delete_user, approve_event, verify_organizer
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



    path('admin/users/', admin_users, name='admin_users'),
path('admin/events/', admin_events, name='admin_events'),
path('admin/report/', generate_report, name='admin_report'),
path('admin/export-users/', export_users_csv, name='export_users'),
path('admin/change-role/<int:user_id>/', change_user_role, name='change_user_role'),
path('admin/delete-user/<int:user_id>/', delete_user, name='delete_user'),
path('approve-event/<int:event_id>/', approve_event, name='approve_event'),
path('verify-organizer/<int:user_id>/', verify_organizer, name='verify_organizer'),

]


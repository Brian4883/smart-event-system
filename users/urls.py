# users/urls.py
from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    password_reset_view,
    admin_dashboard,
    organizer_dashboard,
    attendee_dashboard,
    profile,
    update_profile,
    admin_dashboard,
    admin_events,
    change_user_role, 
    verify_organizer,
    download_users_report,
    download_organizer_report,
    view_user,
    deactivate_user,
    delete_user,
    activate_user
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # AUTH
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # PROFILE
    path('profile/', profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),

    # DASHBOARDS
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('organizer-dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('attendee-dashboard/', attendee_dashboard, name='attendee_dashboard'),

    # PASSWORD RESET
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

      # REPORTS
    path('admin/report/', download_users_report, name='download_report'),
    path('report/events/', download_organizer_report, name='organizer_report'),

     # ADMIN USER MANAGEMENT
    path('admin/events/', admin_events, name='admin_events'),   
    path('admin/change-role/<int:user_id>/', change_user_role, name='change_user_role'),

    # ORGANIZER APPROVAL
    path('verify-organizer/<int:user_id>/', verify_organizer, name='verify_organizer'),

    # USER ACTIONS 
    path('user/<int:user_id>/view/', view_user, name='view_user'),
    path('user/<int:user_id>/deactivate/', deactivate_user, name='deactivate_user'),
    path('user/<int:user_id>/activate/', activate_user, name='activate_user'),
    path('user/<int:user_id>/delete/', delete_user, name='delete_user'),
]


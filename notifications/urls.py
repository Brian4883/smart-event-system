from django.urls import path
from .views import notifications_view, notification_settings

urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('settings/', notification_settings, name='notification_settings'),
]
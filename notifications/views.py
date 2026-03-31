from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications
    })


@login_required
def notification_settings(request):
    return render(request, 'notification_settings.html')
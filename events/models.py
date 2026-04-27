from django.db import models
from django.conf import settings

class Event(models.Model):
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_tickets = models.IntegerField()

    image = models.ImageField(upload_to='events/', null=True, blank=True)

    # 🔥 NEW (IMPORTANT)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
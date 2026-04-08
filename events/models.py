from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    total_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed')
        ],
        default='pending'
    )

    mpesa_checkout_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
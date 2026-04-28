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
    price_details = models.CharField(max_length=200, blank=True, null=True, verbose_name='Price note')

    PAYMENT_METHOD_CHOICES = [
        ('till', 'Till Number'),
        ('phone', 'Phone Number'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True,
        verbose_name='Payment method'
    )
    payment_details = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Payment details',
        help_text='Enter a till number or phone number',
    )

    total_tickets = models.CharField(max_length=100, blank=True, null=True, verbose_name='Capacity')

    image = models.ImageField(upload_to='events/', null=True, blank=True)

    # 🔥 NEW (IMPORTANT)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
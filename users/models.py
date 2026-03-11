from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='attendee'
    )

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
    upload_to='profile_pics/',
    default='default.png',
    blank=True
    )
    
    date_created = models.DateTimeField(
        auto_now_add=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    def save(self, *args, **kwargs):

        if self.is_superuser:
            self.role = 'admin'

        super().save(*args, **kwargs)
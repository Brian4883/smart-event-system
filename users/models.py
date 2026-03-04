from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
        ('staff', 'Gate Staff'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')

    def __str__(self):
        return self.username
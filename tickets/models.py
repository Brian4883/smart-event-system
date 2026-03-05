from django.db import models
from django.conf import settings
from events.models import Event
import qrcode
from io import BytesIO
from django.core.files import File

User = settings.AUTH_USER_MODEL


class Ticket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    ticket_code = models.CharField(max_length=200, unique=True)

    qr_code = models.ImageField(upload_to='tickets_qr', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        qr_data = f"Ticket:{self.ticket_code} Event:{self.event.title}"

        qr_img = qrcode.make(qr_data)

        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')

        filename = f"ticket_{self.ticket_code}.png"

        self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_code
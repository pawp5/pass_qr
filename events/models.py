from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
        Stores the event information
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = models.ManyToManyField(User, through='Pass')

    def __str__(self):
        return self.name    
    
    
class Pass(models.Model):
    """
        Stores the ticket information for an event
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to='qrcodes/')
    # qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta:
        models.UniqueConstraint(fields=['event', 'user'], name='unique_event_pass')

    def __str__(self):
        return f'{self.user.username} - {self.event.name}'

from django.db import models

# Create your models here.
class Event(models.Model):
    """
        Stores the event information
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
    
class Pass(models.Model):
    """
        Stores the ticket information for an event
    """
    for_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    qrcode = models.ImageField(upload_to='qrcodes/')
    # qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

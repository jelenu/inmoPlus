from django.db import models
from properties.models import Property
from clients.models import Client
from django.conf import settings

class visits(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="visits"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="visits"
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visits"
    )
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])
    notes = models.TextField(blank=True, null=True)
    

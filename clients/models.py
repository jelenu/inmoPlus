from django.db import models
from django.conf import settings

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients"
    )

    def __str__(self):
        return f"{self.name} ({self.email})"

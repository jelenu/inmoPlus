from django.db import models
from django.conf import settings

class Contract(models.Model):
    TYPE_CHOICES = [
        ('rental', 'Rental'),
        ('sale', 'Sale'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('signed', 'Signed'),
        ('cancelled', 'Cancelled'),
    ]

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='contracts')
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='contracts')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    document = models.FileField(upload_to='contracts/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} contract for {self.property} - {self.client}"

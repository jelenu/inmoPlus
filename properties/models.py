from django.conf import settings
from django.db import models
import os
class Property(models.Model):

    #Choices for property status
    STATUS_CHOICES = [
        ("available", "Disponible"),
        ("sold", "Vendida"),
        ("rented", "Alquilada"),
        ("reserved", "Reservada"),
    ]

    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available", verbose_name="Estado"
    )
    address = models.CharField(max_length=255, verbose_name="Dirección")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitud")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitud")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # ForeignKey to the user model
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
        verbose_name="Propietario"
    )

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Propiedad"
    )
    image = models.ImageField(
        upload_to="property_images/",
        verbose_name="Imagen"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de subida"
    )

    def __str__(self):
        return f"Imagen de {self.property.title}"

    def delete(self, *args, **kwargs):
        if self.image and self.image.path and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


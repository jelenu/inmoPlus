from django.db import models

# Create your models here.

class Property(models.Model):
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

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images", verbose_name="Propiedad"
    )
    image = models.ImageField(upload_to="property_images/", verbose_name="Imagen")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de subida")

    def __str__(self):
        return f"Imagen de {self.property.title}"

from rest_framework import serializers
from .models import Property, PropertyImage
from django.core.exceptions import PermissionDenied
import os

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'uploaded_at']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    delete_images = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'status', 'address',
            'latitude', 'longitude', 'created_at', 'updated_at', 'images', 'delete_images'
        ]

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        property_instance = Property.objects.create(**validated_data)
        for image_data in images_data:
            PropertyImage.objects.create(property=property_instance, image=image_data)
        return property_instance

    def update(self, instance, validated_data):
        # Obtén las nuevas imágenes de la solicitud
        images_data = self.context['request'].FILES.getlist('images')

        # Eliminar imágenes especificadas
        delete_images = validated_data.pop('delete_images', [])
        for image_id in delete_images:
            try:
                image_instance = PropertyImage.objects.get(id=image_id, property=instance)
                # Elimina el archivo físico de la carpeta
                if image_instance.image and os.path.isfile(image_instance.image.path):
                    os.remove(image_instance.image.path)
                # Elimina la relación en la base de datos
                image_instance.delete()
            except PropertyImage.DoesNotExist:
                raise PermissionDenied("No tienes permiso para eliminar esta imagen.")

        # Actualiza los campos de la propiedad
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Agrega las nuevas imágenes sin eliminar las existentes
        for image_data in images_data:
            PropertyImage.objects.create(property=instance, image=image_data)

        return instance
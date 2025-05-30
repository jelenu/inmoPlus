from rest_framework import serializers
from .models import Property, PropertyImage
from django.core.exceptions import PermissionDenied, ValidationError
import os


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'property', 'image']


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    delete_images = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    # Read only fields
    owner_first_name = serializers.CharField(source='owner.first_name', read_only=True)
    owner_last_name = serializers.CharField(source='owner.last_name', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'status', 'address',
            'latitude', 'longitude', 'created_at', 'updated_at', 'images', 'delete_images',
            'owner_first_name', 'owner_last_name'
        ]

    # Create method to handle the creation of Property and its images
    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')

        # Validate all images before creating the property
        for image_data in images_data:
            if not image_data.content_type.startswith('image/'):
                raise serializers.ValidationError("Only image files are allowed.")

        # Create the property only if all images are valid
        property_instance = Property.objects.create(**validated_data)
        for image_data in images_data:
            PropertyImage.objects.create(property=property_instance, image=image_data)
        return property_instance

    # Update method to handle the update of Property and its images
    def update(self, instance, validated_data):
        # Obtén las nuevas imágenes de la solicitud
        images_data = self.context['request'].FILES.getlist('images')

        # Validate all new images before updating the property
        for image_data in images_data:
            if not image_data.content_type.startswith('image/'):
                raise serializers.ValidationError("Only image files are allowed.")

        # Delete images if specified
        delete_images = validated_data.pop('delete_images', [])
        for image_id in delete_images:
            try:
                image_instance = PropertyImage.objects.get(id=image_id, property=instance)
                # Delete the image file from the filesystem
                if image_instance.image and os.path.isfile(image_instance.image.path):
                    os.remove(image_instance.image.path)
                # Delete the image instance from the database
                image_instance.delete()
            except PropertyImage.DoesNotExist:
                raise PermissionDenied("No tienes permiso para eliminar esta imagen.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Add new images
        for image_data in images_data:
            PropertyImage.objects.create(property=instance, image=image_data)

        return instance
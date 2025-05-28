from rest_framework import serializers
from .models import Favorite, ContactForm
from properties.models import Property
from properties.serializers import PropertySerializer

class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'property', 'created_at']

class ContactFormSerializer(serializers.ModelSerializer):
    property_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ContactForm
        fields = ['id', 'name', 'email', 'phone', 'message', 'property_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_property_id(self, value):
        if not Property.objects.filter(id=value).exists():
            raise serializers.ValidationError("Property with this ID does not exist.")
        return value

    def create(self, validated_data):
        property_id = validated_data.pop('property_id')
        property_instance = Property.objects.get(id=property_id)
        return ContactForm.objects.create(property=property_instance, **validated_data)

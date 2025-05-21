from rest_framework import serializers
from .models import visits
from clients.models import Client
from properties.models import Property
from django.utils import timezone

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = visits
        fields = ['id', 'property', 'client', 'agent', 'date', 'status', 'notes']

    def validate(self, data):
        request = self.context['request']
        user = request.user

        # Validate date is not in the past
        if data['date'] < timezone.now():
            raise serializers.ValidationError("Visit date cannot be in the past.")

        # Validate client exists and belongs to agent
        client = data.get('client')
        if not Client.objects.filter(id=client.id, agent=user).exists():
            raise serializers.ValidationError("Client does not exist or does not belong to you.")

        # Validate property exists and belongs to agent
        property = data.get('property')
        if not Property.objects.filter(id=property.id, owner=user).exists():
            raise serializers.ValidationError("Property does not exist or does not belong to you.")

        return data

    def create(self, validated_data):
        validated_data['agent'] = self.context['request'].user
        return super().create(validated_data)
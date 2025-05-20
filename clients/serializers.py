from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'notes', 'agent']

    def validate_email(self, value):
        if Client.objects.filter(email=value).exists():
            raise serializers.ValidationError("A client with this email already exists.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['agent'] = user
        return super().create(validated_data)
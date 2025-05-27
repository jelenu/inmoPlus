from rest_framework import serializers
from .models import Contract
from properties.models import Property
from clients.models import Client
from django.utils import timezone

class PropertySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'status']

class ClientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email']

class ContractSerializer(serializers.ModelSerializer):
    property_summary = PropertySummarySerializer(source='property', read_only=True)
    client_summary = ClientSummarySerializer(source='client', read_only=True)
    document = serializers.FileField(required=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'property', 'property_summary', 'client', 'client_summary', 'agent',
            'type', 'price', 'start_date', 'end_date', 'document', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['agent', 'created_at', 'updated_at', 'property_summary', 'client_summary']

    def validate(self, data):
        user = self.context['request'].user

        instance = getattr(self, 'instance', None)

        start_date = data.get('start_date') or (instance.start_date if instance else None)
        end_date = data.get('end_date')  or (instance.end_date if instance else None)

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date cannot be before start date."})


        property = data.get('property')
        client = data.get('client')
        if user.role == 'agent':
            if property and property.owner != user:
                raise serializers.ValidationError("You can only create contracts for your own properties.")
            if client and client.agent != user:
                raise serializers.ValidationError("You can only create contracts for your own clients.")

        if property and property.status != 'available':
            raise serializers.ValidationError("Property must be available to create a contract.")

        if Contract.objects.filter(property=property, status='signed').exists():
            raise serializers.ValidationError("There is already a signed contract for this property.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['agent'] = user

        contract = super().create(validated_data)

        if contract.status == 'signed':
            if contract.type == 'rental':
                contract.property.status = 'rented'
            elif contract.type == 'sale':
                contract.property.status = 'sold'
            contract.property.save()

        return contract

    def update(self, instance, validated_data):
        prev_status = instance.status
        contract = super().update(instance, validated_data)

        if contract.status == 'signed' and prev_status != 'signed':
            if contract.type == 'rental':
                contract.property.status = 'rented'
            elif contract.type == 'sale':
                contract.property.status = 'sold'
            contract.property.save()
        return contract
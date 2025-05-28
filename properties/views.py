from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property
from .serializers import PropertySerializer
from .permissions import IsOwnerOrAdmin, IsAgentOrAdmin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
@extend_schema(tags=["properties"])
class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

@extend_schema(tags=["properties"])
class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(tags=["properties"])
class PropertyCreateView(CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAgentOrAdmin]  # Apply the custom permission

    def perform_create(self, serializer):
        # Automatically set the owner to the authenticated user
        serializer.save(owner=self.request.user)

@extend_schema(tags=["properties"])
class PropertyUpdateView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(tags=["properties"])
class PropertyDeleteView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrAdmin]

from django.shortcuts import render
from rest_framework import generics
from .models import Visit
from .serializers import VisitSerializer
from .permissions import IsAgentOrAdmin
from drf_spectacular.utils import extend_schema
@extend_schema(tags=["Visits"])
class VisitListCreateView(generics.ListCreateAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAgentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Visit.objects.all()
        return Visit.objects.filter(agent=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

@extend_schema(tags=["Visits"])
class VisitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAgentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Visit.objects.all()
        return Visit.objects.filter(agent=user)

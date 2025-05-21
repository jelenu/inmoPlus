from django.shortcuts import render
from rest_framework import generics
from .models import visits
from .serializers import VisitSerializer
from .permissions import IsAgentOrAdmin

class VisitListCreateView(generics.ListCreateAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAgentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return visits.objects.all()
        return visits.objects.filter(agent=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class VisitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAgentOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return visits.objects.all()
        return visits.objects.filter(agent=user)

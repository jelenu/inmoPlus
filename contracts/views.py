from django.shortcuts import render
from rest_framework import generics
from .models import Contract
from .serializers import ContractSerializer
from .permissions import IsAgentOrAdminContract

class ContractListCreateView(generics.ListCreateAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAgentOrAdminContract]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Contract.objects.all()
        return Contract.objects.filter(agent=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class ContractRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = [IsAgentOrAdminContract]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Contract.objects.all()
        return Contract.objects.filter(agent=user)

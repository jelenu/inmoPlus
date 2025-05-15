from rest_framework import generics
from .models import Client
from .serializers import ClientSerializer
from .permissions import IsAgentOrAdminClient

class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAgentOrAdminClient]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Client.objects.all()
        return Client.objects.filter(agent=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAgentOrAdminClient]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Client.objects.all()
        return Client.objects.filter(agent=user)

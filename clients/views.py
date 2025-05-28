from rest_framework import generics
from .models import Client
from .serializers import ClientSerializer
from .permissions import IsAgentOrAdminClient
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Clients"])
class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAgentOrAdminClient]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Client.objects.none()

        
        user = self.request.user
        if user.role == 'admin':
            return Client.objects.all()
        return Client.objects.filter(agent=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)
@extend_schema(tags=["Clients"])
class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAgentOrAdminClient]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Client.objects.none()
        user = self.request.user
        if user.role == 'admin':
            return Client.objects.all()
        return Client.objects.filter(agent=user)

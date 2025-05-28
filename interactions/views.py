from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Favorite, ContactForm
from .serializers import FavoriteSerializer, ContactFormSerializer
from properties.models import Property
from drf_spectacular.utils import extend_schema
from .permissions import IsViewer

@extend_schema(tags=["Favorites"])
class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsViewer]

    def list(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        user = request.user
        try:
            property = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({"detail": "Property not found."}, status=404)

        favorite, created = Favorite.objects.get_or_create(user=user, property=property)

        if not created:
            favorite.delete()
            return Response({"status": "removed"})
        return Response({"status": "added"})

@extend_schema(tags=["Contact"])
class ContactFormCreateView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [IsViewer]

@extend_schema(tags=["Contact"])
class ContactFormListView(generics.ListAPIView):
    serializer_class = ContactFormSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ContactForm.objects.all()
        elif user.role == 'agent':
            return ContactForm.objects.filter(property__owner=user)

        return ContactForm.objects.none()

@extend_schema(tags=["Contact"])
class ContactFormDetailView(generics.RetrieveAPIView):
    serializer_class = ContactFormSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ContactForm.objects.all()
        elif user.role == 'agent':
            return ContactForm.objects.filter(property__owner=user)
        return ContactForm.objects.none()
@extend_schema(tags=["Contact"])
class ContactFormDestroyView(generics.DestroyAPIView):
    serializer_class = ContactFormSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ContactForm.objects.all()
        elif user.role == 'agent':
            return ContactForm.objects.filter(property__owner=user)
        return ContactForm.objects.none()


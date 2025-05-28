from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer
from properties.models import Property
from drf_spectacular.utils import extend_schema
@extend_schema(tags=["Favorites"])
class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

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

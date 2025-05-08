from django.shortcuts import render
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import RegisterSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

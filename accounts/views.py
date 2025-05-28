from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView as SimpleJWTLoginView, TokenRefreshView as SimpleJWTRefreshView
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Accounts"])
class TokenObtainPairView(SimpleJWTLoginView):
    pass

@extend_schema(tags=["Accounts"])
class TokenRefreshView(SimpleJWTRefreshView):
    pass

@extend_schema(tags=["Accounts"])
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=["Accounts"], responses=UserSerializer)
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

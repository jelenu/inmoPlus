from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from accounts.models import CustomUser
from datetime import timedelta

class TokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
        )

    def test_token_refresh_valid(self):
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}
        url = reverse("token_refresh")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_expired(self):
        refresh = RefreshToken.for_user(self.user)
        refresh.set_exp(lifetime=timedelta(seconds=-1))
        data = {"refresh": str(refresh)}
        url = reverse("token_refresh")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertIn("expired", response.data["detail"].lower())

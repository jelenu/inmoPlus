from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class AccountsTests(TestCase):
    def setUp(self):
        # * Create a test user
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User",
        )
        self.client = APIClient()

    # ! Test user registration
    def test_register_user(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post("/api/accounts/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # * Ensure a new user is created

    # ! Test user registration with invalid data
    def test_register_user_invalid_data(self):
        data = {
            "email": "invalid-email",
            "password": "",
            "first_name": "",
            "last_name": "User",
        }
        response = self.client.post("/api/accounts/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
        
    # ! Test user registration with existing email
    def test_register_user_duplicate_email(self):
        data = {
            "email": "testuser@example.com",
            "password": "newpassword123",
            "first_name": "Duplicate",
            "last_name": "User",
        }
        response = self.client.post("/api/accounts/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    # ! Test user login
    def test_login_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post("/api/accounts/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # * Ensure access token is returned
        self.assertIn("refresh", response.data)  # * Ensure refresh token is returned

    # ! Test retrieving user details (MeView)
    def test_get_user_details(self):
        self.client.force_authenticate(user=self.user)  # * Authenticate the test user
        response = self.client.get("/api/accounts/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)

    # ! Test unauthorized access to MeView
    def test_unauthorized_access_me_view(self):
        response = self.client.get("/api/accounts/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test token refresh with a valid token
    def test_token_refresh_valid(self):
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}  
        response = self.client.post("/api/accounts/token/refresh/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertIn("access", response.data)

    # ! Test token refresh with an expired token
    def test_token_refresh_expired(self):
        # * Generate a refresh token and manually set it to be expired
        refresh = RefreshToken.for_user(self.user)
        refresh.set_exp(lifetime=timedelta(seconds=-1))  # Expire the token immediately
        data = {"refresh": str(refresh)}
        response = self.client.post("/api/accounts/token/refresh/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Token is expired")

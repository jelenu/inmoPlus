from django.test import TestCase
from rest_framework import status
from accounts.models import CustomUser
from properties.models import Property
from django.urls import reverse


class PropertiesListTests(TestCase):
    def setUp(self):
        # * Create a user
        self.user = CustomUser.objects.create_user(
            email="user@test.com",
            password="userpassword123",
            first_name="Test",
            last_name="User",
        )

        # * Create a property associated with the user
        self.property = Property.objects.create(
            title="Test Property",
            description="Test Description",
            price=100000,
            owner=self.user,
        )
    
    # ! Test for an authenticated user accessing properties list
    def test_authenticated_user_access_properties_list(self):
        jwt_token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("properties-list")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    # ! Test for unauthenticated user (no token)
    def test_unauthenticated_user_access_properties_list(self):
        url = reverse("properties-list")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for authenticated user accessing property detail
    def test_authenticated_user_access_property_detail(self):
        jwt_token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("property-detail", args=[self.property.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.data), 0)

    # ! Test for unauthenticated user accessing property detail
    def test_unauthenticated_user_access_property_detail(self):
        url = reverse("property-detail", args=[self.property.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
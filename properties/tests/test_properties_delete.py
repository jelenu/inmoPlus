from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from properties.models import Property, PropertyImage
from django.urls import reverse

class PropertiesDeleteTests(TestCase):
    def setUp(self):
        # * Create viewer user
        self.viewer_user = CustomUser.objects.create_user(
            email="viewer@test.com",
            password="viewerpassword123",
            first_name="Viewer",
            last_name="User",
        )
        self.viewer_user.role = "viewer"
        self.viewer_user.save()

        # * Create agent1 user
        self.agent1_user = CustomUser.objects.create_user(
            email="agent1@test.com",
            password="agent1password123",   
            first_name="Agent1",
            last_name="User",
        )
        self.agent1_user.role = "agent"
        self.agent1_user.save()

        # * Create agent2 user
        self.agent2_user = CustomUser.objects.create_user(
            email="agent2@test.com",
            password="agent2password123",
            first_name="Agent2",
            last_name="User",
        )
        self.agent2_user.role = "agent"
        self.agent2_user.save()

        # * Create admin user
        self.admin_user = CustomUser.objects.create_user(
            email="admin@test.com",
            password="adminpassword123",
            first_name="Admin",
            last_name="User",
        )
        self.admin_user.role = "admin"
        self.admin_user.save()

        # * Create a property for agent1
        self.property = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent1_user,
        )

        # * ApiClient instance
        self.client = APIClient()

    # ! Helper function to get JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    # ! Test for agent1 user deleting their own property
    def test_agent1_user_delete_own_property(self):
        jwt_token = self.get_jwt_token(self.agent1_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-delete", args=[self.property.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 0)

    # ! Test for agent2 user trying to delete agent1's property
    def test_agent2_user_delete_agent1_property(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-delete", args=[self.property.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 1)
    
    # ! Test for admin user deleting any property
    def test_admin_user_delete_property(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-delete", args=[self.property.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 0)
    
    # ! Test for viewer user trying to delete a property
    def test_viewer_user_delete_property(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-delete", args=[self.property.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 1)
    
    # ! Test for unauthenticated user trying to delete a property
    def test_unauthenticated_user_delete_property(self):
        url = reverse("property-delete", args=[self.property.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Property.objects.count(), 1)
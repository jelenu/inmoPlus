from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from properties.models import Property, PropertyImage
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from common_tests.base import BaseUserTestCase
class PropertiesDeleteTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()

        # * Create agent2 user
        self.agent2_user = CustomUser.objects.create_user(
            email="agent2@test.com",
            password="agent2password123",
            first_name="Agent2",
            last_name="User",
            role="agent",
        )
        
        # * Create a property for agent
        self.property = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent_user,
        )
        # * Add an initial image to the property
        self.initial_image = PropertyImage.objects.create(
            property=self.property,
            image=SimpleUploadedFile("initial_image.jpg", b"initial_image_data", content_type="image/jpeg"),
        )
    
    # ! Test for agent user deleting their own property
    def test_agent_user_delete_own_property(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-delete", args=[self.property.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 0)

    # ! Test for agent2 user trying to delete agent's property
    def test_agent2_user_delete_agent_property(self):
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
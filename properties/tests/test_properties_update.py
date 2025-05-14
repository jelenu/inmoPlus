from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from properties.models import Property, PropertyImage
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class PropertiesUpdateTests(TestCase):
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

        # * Add an initial image to the property
        self.initial_image = PropertyImage.objects.create(
            property=self.property,
            image=SimpleUploadedFile("initial_image.jpg", b"initial_image_data", content_type="image/jpeg"),
        )

        # * ApiClient instance
        self.client = APIClient()

    # ! Helper function to get JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    # ! Test for agent1 user updating their own property
    def test_agent1_user_update_own_property(self):
        jwt_token = self.get_jwt_token(self.agent1_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        # Creating a new dummy image
        new_image = SimpleUploadedFile("new_image.jpg", b"new_image_data", content_type="image/jpeg")

        url = reverse("property-update", args=[self.property.pk])
        data = {
            "title": "Updated Property",
            "description": "Updated Property Description",
            "images": [new_image],  # Add the new image
            "delete_images": [self.initial_image.id],  # Specify the image to delete
        }

        response = self.client.patch(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()

        # Check that the property was updated
        self.assertEqual(self.property.title, "Updated Property")
        self.assertEqual(self.property.description, "Updated Property Description")

        # Check that the initial image was deleted
        self.assertFalse(PropertyImage.objects.filter(id=self.initial_image.id).exists())

        # Check that the new image was added
        new_images = PropertyImage.objects.filter(property=self.property)
        self.assertEqual(new_images.count(), 1)
        self.assertIn("new_image", new_images.first().image.name)

    # ! Test for agent2 user trying to update agent1's property
    def test_agent2_user_update_agent1_property(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-update", args=[self.property.pk])
        data = {
            "title": "Malicious Update",
            "description": "Malicious Update Description",
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.property.refresh_from_db()

        # Check that the property was not updated
        self.assertNotEqual(self.property.title, "Malicious Update")

    # ! Test for viewer user trying to update a property
    def test_viewer_user_update_property(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-update", args=[self.property.pk])
        data = {
            "title": "Malicious Update",
            "description": "Malicious Update Description",
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.property.refresh_from_db()

        # Check that the property was not updated
        self.assertNotEqual(self.property.title, "Malicious Update")

    # ! Test for admin user updating any property
    def test_admin_user_update_property(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-update", args=[self.property.pk])
        data = {
            "title": "Admin Update",
            "description": "Admin Update Description",
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.property.refresh_from_db()

        # Check that the property was updated
        self.assertEqual(self.property.title, "Admin Update")
        self.assertEqual(self.property.description, "Admin Update Description")
from rest_framework import status
from properties.models import Property
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from common_tests.base import BaseUserTestCase
class PropertiesCreateTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()
    
    # ! Test for agent user creating a property
    def test_agent_user_create_property(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        # Creating a dummy image
        image = SimpleUploadedFile("image.jpg", b"image_data", content_type="image/jpeg")
        
        url = reverse("property-create")
        data = {
            "title": "New Property",
            "description": "New Property Description",
            "price": 150000,
            "address": "123 New Street",
            "images": [image],

        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.get().title, "New Property")
        self.assertEqual(Property.objects.get().owner.first_name, "Agent")
        self.assertEqual(Property.objects.get().images.count(), 1)


    # ! Test for viwer user trying to create a property
    def test_viewer_user_create_property(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-create")
        data = {
            "title": "New Property",
            "description": "New Property Description",
            "price": 150000,
            "address": "123 New Street",

        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Property.objects.count(), 0)

    # ! Test for agent trying to create a property without required fields
    def test_agent_user_create_property_without_required_fields(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("property-create")
        data = {
            "title": "New Property",
            "description": "New Property Description",
            # Missing required fields
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Property.objects.count(), 0)

    
    # !Test for agent trying to create a property with invalid image
    def test_agent_user_create_property_with_invalid_image(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        # Creating a dummy invalid image
        invalid_image = SimpleUploadedFile("invalid.txt", b"invalid_data", content_type="text/plain")
        
        url = reverse("property-create")
        data = {
            "title": "New Property",
            "description": "New Property Description",
            "price": 150000,
            "address": "123 New Street",
            "images": [invalid_image],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Property.objects.count(), 0)

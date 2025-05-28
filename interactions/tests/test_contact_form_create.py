from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from common_tests.base import BaseUserTestCase
from properties.models import Property

class ContactFormCreateTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()

        # * Create viewer user
        self.viewer_user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User",
        )
        # * Create property
        self.property = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent_user,
        )
    
    # ! Test for viewer user creating a contact form
    def test_viewer_user_create_contact_form(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-create")
        data = {
            "name": "Test User",
            "email": "viewer@test.com",
            "message": "Interested in this property.",
            "property_id": self.property.id,
        
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    # ! Test for viewer user creating a contact form with invalid property ID
    def test_viewer_user_create_contact_form_invalid_property(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-create")
        data = {
            "name": "Test User",
            "email": "viewer@test.com",
            "message": "Interested in this property.",
            "property_id": 9999,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Property with this ID does not exist.", response.data['property_id'])

    # ! Test for viewer user creating a contact form without required fields
    def test_viewer_user_create_contact_form_missing_fields(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-create")
        data = {
            "name": "Test User",
            "email": "viewer@test.com",
            "message": "Interested in this property.",
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ! Test for unauthenticated user creating a contact form
    def test_unauthenticated_user_create_contact_form(self):
        url = reverse("contact-form-create")
        data = {
            "name": "Test User",
            "email": "viewer@test.com",
            "message": "Interested in this property.",
            "property_id": 9999,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for agent user creating a contact form
    def test_agent_user_create_contact_form(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-create")
        data = {
            "name": "Test User",
            "email": "viewer@test.com",
            "message": "Interested in this property.",
            "property_id": 9999,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from common_tests.base import BaseUserTestCase
from properties.models import Property
from interactions.models import ContactForm

class ContactFormListDetailTests(BaseUserTestCase):
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

        # * Create contact form
        self.contact_form = ContactForm.objects.create(
            name= "Test User",
            email = "viewer@test.com",
            message = "Interested in this property.",
            property_id = self.property.id,
        )

    # ! Test for agent user listing contact forms
    def test_agent_user_list_contact_forms(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.contact_form.name)

    # ! Test for admin user listing contact forms
    def test_admin_user_list_contact_forms(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.contact_form.name)

    # ! Test for viewer user trying to list contact forms
    def test_viewer_user_list_contact_forms(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for agent user retrieving a specific contact form
    def test_agent_user_retrieve_contact_form(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-detail", args=[self.contact_form.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.contact_form.name)
    
    # ! Test for admin user retrieving a specific contact form
    def test_admin_user_retrieve_contact_form(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-detail", args=[self.contact_form.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.contact_form.name)
    
    # ! Test for viewer user trying to retrieve a specific contact form
    def test_viewer_user_retrieve_contact_form(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-detail", args=[self.contact_form.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ! Test for unauthenticated user trying to retrieve a specific contact form
    def test_unauthenticated_user_retrieve_contact_form(self):
        url = reverse("contact-form-detail", args=[self.contact_form.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for agent user trying to retrieve a non-existent contact form
    def test_agent_user_retrieve_non_existent_contact_form(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-detail", args=[9999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
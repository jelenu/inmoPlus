from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from common_tests.base import BaseUserTestCase
from properties.models import Property
from interactions.models import ContactForm

class ContactFormDeleteTests(BaseUserTestCase):
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
    
        # * Create agent2 user
        self.agent2_user = CustomUser.objects.create_user(
            email="agent2@test.com",
            password="agentpassword123",
            first_name="Agent",
            last_name="Two",
            role="agent"
        )

    # ! Test for agent user deleting a contact form
    def test_agent_user_delete_contact_form(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-delete", args=[self.contact_form.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ContactForm.objects.filter(id=self.contact_form.id).exists())

    # ! Test for admin user deleting a contact form
    def test_admin_user_delete_contact_form(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-delete", args=[self.contact_form.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ContactForm.objects.filter(id=self.contact_form.id).exists())
    
    # ! Test for viewer user trying to delete a contact form
    def test_viewer_user_delete_contact_form(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-delete", args=[self.contact_form.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(ContactForm.objects.filter(id=self.contact_form.id).exists())
    
    # ! Test for agent2 user trying to delete a contact form they do not own
    def test_agent2_user_delete_contact_form(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-delete", args=[self.contact_form.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(ContactForm.objects.filter(id=self.contact_form.id).exists())

    # ! Test for unauthenticated user trying to delete a contact form
    def test_unauthenticated_user_delete_contact_form(self):
        url = reverse("contact-form-delete", args=[self.contact_form.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(ContactForm.objects.filter(id=self.contact_form.id).exists())
    
    # ! Test for deleting a non-existent contact form
    def test_delete_non_existent_contact_form(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contact-form-delete", args=[9999])  # Non-existent ID
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(ContactForm.objects.filter(id=9999).exists())

    # ! Test for unauthenticated user trying to delete a contact form
    def test_unauthenticated_user_delete_contact_form(self):
        url = reverse("contact-form-delete", args=[self.contact_form.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(ContactForm.objects.filter(id=self.contact_form.id).exists())
    
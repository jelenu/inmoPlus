from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from common_tests.base import BaseUserTestCase
from properties.models import Property
from visits.models import Visit
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

class VisitsDeleteTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()

        # * Create Agent2 User
        self.agent2_user = CustomUser.objects.create_user(
            email="agent2@test.com",
            password="agent2password123",
            first_name="Agent2",
            last_name="User",
            role="agent",
        )

        # * Create Client with agent
        self.client1 = Client.objects.create(
            name="Client1",
            email="client1@test.com",
            phone="123456789",
            notes="Notes",
            agent=self.agent_user,

        )
        # * Create a property for agent
        self.property = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent_user,
        )

        # * Create a visit
        self.visit = Visit.objects.create(
            client=self.client1,
            property=self.property,
            date=timezone.now() + timedelta(days=1),
            status="scheduled",
            agent=self.agent_user,
        )

    # ! Test for Admin user deleting a visit
    def test_admin_user_delete_visit(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Visit.objects.filter(id=self.visit.id).exists())

    # ! Test for Agent user deleting a visit
    def test_agent_user_delete_visit(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Visit.objects.filter(id=self.visit.id).exists())


    # ! Test for Agent2 user trying to delete a visit of another agent
    def test_agent2_user_delete_visit_of_another_agent(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Visit.objects.filter(id=self.visit.id).exists())

    # ! Test for deleting a visit that does not exist
    def test_delete_non_existent_visit(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": 9999})  # Non-existent visit ID

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Visit.objects.filter(id=9999).exists())

    # ! Test for Viewer user trying to delete a visit
    def test_viewer_user_delete_visit(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Visit.objects.filter(id=self.visit.id).exists())

    # ! Test for unauthenticated user trying to delete a visit
    def test_unauthenticated_user_delete_visit(self):
        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Visit.objects.filter(id=self.visit.id).exists())


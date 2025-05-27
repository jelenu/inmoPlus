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


class VisitsUpdateTests(BaseUserTestCase):
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

    # ! Test for Admin user updating a visit
    def test_admin_user_update_visit(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        data = {
            "status": "completed",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.visit.refresh_from_db()
        self.assertEqual(self.visit.status, "completed")

    # ! Test for Agent user updating a visit
    def test_agent_user_update_visit(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        data = {
            "status": "completed",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.visit.refresh_from_db()
        self.assertEqual(self.visit.status, "completed")

    # ! Test for Agent2 user trying to update a visit of another agent
    def test_agent2_user_update_visit_of_another_agent(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        data = {
            "status": "completed",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ! Test for Viewer user trying to update a visit
    def test_viewer_user_update_visit(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        data = {
            "status": "completed",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ! Test for unauthenticated user trying to update a visit
    def test_unauthenticated_user_update_visit(self):
        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        data = {
            "status": "completed",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for updating visit with invalid date
    def test_update_visit_with_invalid_date(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-detail", kwargs={"pk": self.visit.id})

        # Set date in the past
        data = {
            "date": timezone.now() - timedelta(days=1),
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Visit date cannot be in the past.", str(response.data))

    
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

class VisitsCreateTests(BaseUserTestCase):
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
            email="client@test.com",
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

    # ! Test for Admin user creating a visit
    def test_admin_user_create_visit(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-list-create")

        data = {
            "client": self.client1.id,
            "property": self.property.id,
            "date": timezone.now() + timedelta(days=1),
            "status": "scheduled",
        }

        response = self.client.post(url, data, format="json")
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ! Test for Agent user creating a visit
    def test_agent_user_create_visit(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-list-create")

        data = {
            "client": self.client1.id,
            "property": self.property.id,
            "date": timezone.now() + timedelta(days=1),
            "status": "scheduled",
        }

        response = self.client.post(url, data, format="json")
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ! Test for Agent2 user trying to create a visit with another agent's client
    def test_agent2_user_create_visit_with_another_agents_client(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-list-create")

        data = {
            "client": self.client1.id,  # Client belongs to agent_user, not agent2_user
            "property": self.property.id,
            "date": timezone.now() + timedelta(days=1),
            "status": "scheduled",
        }

        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Client does not exist or does not belong to you.", str(response.data))

    # ! Test for Viewer user trying to create a visit
    def test_viewer_user_create_visit(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-list-create")

        data = {
            "client": self.client1.id,
            "property": self.property.id,
            "date": timezone.now() + timedelta(days=1),
            "status": "scheduled",
        }

        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user trying to create a visit
    def test_unauthenticated_user_create_visit(self):
        url = reverse("visit-list-create")

        data = {
            "client": self.client1.id,
            "property": self.property.id,
            "date": timezone.now() + timedelta(days=1),
            "status": "scheduled",
        }

        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for creating a visit with past date
    def test_create_visit_with_past_date(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("visit-list-create")

        data = {
            "client": self.client1.id,
            "property": self.property.id,
            "date": timezone.now() - timedelta(days=1),  # Past date
            "status": "scheduled",
        }

        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Visit date cannot be in the past.", str(response.data))
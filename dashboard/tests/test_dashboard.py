from rest_framework import status
from django.urls import reverse
from clients.models import Client
from properties.models import Property
from contracts.models import Contract
from visits.models import Visit
from common_tests.base import BaseUserTestCase
from django.utils import timezone
from datetime import timedelta

class DashboardTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()
        # * Create a client for testing
        self.client1 = Client.objects.create(
            name="Client1",
            email="client@test.com",
            phone="123456789",
            notes="Notes",
            agent=self.agent_user,
        )
        # * Create a second client for testing
        self.client2 = Client.objects.create(
            name="Client2",
            email="client2@test.com",
            phone="987654321",
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

        # * Create second property for agent
        self.property2 = Property.objects.create(
            title="Property 2",
            description="Property 2 Description",
            price=200000,
            address="456 Property Avenue",
            owner=self.agent_user,
        )

        # * Create a contract for the first client
        self.contract = Contract.objects.create(
            property=self.property,
            client=self.client1,
            agent=self.agent_user,
            type='rental',
            price=1000.00,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            document=None,
        )

        # * Create a visit
        self.visit = Visit.objects.create(
            client=self.client1,
            property=self.property,
            date=timezone.now() + timedelta(days=1),
            status="scheduled",
            agent=self.agent_user,
        )

    # ! Test for Admin user accessing the dashboard
    def test_admin_user_dashboard(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("dashboard")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_clients", response.data)
        self.assertIn("total_properties", response.data)
        self.assertIn("total_contracts", response.data)

    # ! Test for Agent user accessing the dashboard
    def test_agent_user_dashboard(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("dashboard")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_clients", response.data)
        self.assertIn("total_properties", response.data)
        self.assertIn("total_contracts", response.data)
    
    #! Test for Viewer user trying to access the dashboard
    def test_viewer_user_dashboard(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("dashboard")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("total_clients", response.data)
        self.assertNotIn("total_properties", response.data)
        self.assertNotIn("total_contracts", response.data)
        self.assertNotIn("total_visits", response.data)

    # ! Test for unauthenticated user trying to access the dashboard
    def test_unauthenticated_user_dashboard(self):
        url = reverse("dashboard")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("total_clients", response.data)
        self.assertNotIn("total_properties", response.data)
        self.assertNotIn("total_contracts", response.data)
        self.assertNotIn("total_visits", response.data)






from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from common_tests.base import BaseUserTestCase

class ClientsUpdateTests(BaseUserTestCase):
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

    # ! Test for Admin user updating a client
    def test_admin_user_update_client(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])
        data = {
            "email": "updatedemail@test.com",
            "notes": "Updated notes",
            "agent": self.agent2_user.id,
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.agent, self.agent2_user)

    # ! Test for Agent user updating a client
    def test_agent_user_update_client(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])
        data = {
            "email": "updatedemail@test.com",
            "notes": "Updated notes",
            "agent": self.agent2_user.id,
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client1.refresh_from_db()
        self.assertEqual(self.client1.agent, self.agent2_user)

    # ! Test for Agent2 user trying to update a client
    def test_agent2_user_update_client(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])
        data = {
            "email": "updatedemail@test.com",
            "notes": "Updated notes",
            "agent": self.agent2_user.id,
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ! Test for Viewer user trying to update a client
    def test_viewer_user_update_client(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])
        data = {
            "email": "updatedemail@test.com",
            "notes": "Updated notes",
            "agent": self.agent2_user.id,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user trying to update a client
    def test_unauthenticated_user_update_client(self):
        url = reverse("client-detail", args=[self.client1.id])
        data = {
            "email": "updatedemail@test.com",
            "notes": "Updated notes",
            "agent": self.agent2_user.id,
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for Agent user updating a client with existing email
    def test_agent_user_update_client_with_existing_email(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])
        data = {
            "email": self.client1.email,
            "notes": "Updated notes",
            "agent": self.agent2_user.id,
        }

        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


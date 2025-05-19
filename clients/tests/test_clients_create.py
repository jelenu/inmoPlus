from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from common_tests.base import BaseUserTestCase

class ClientsCreateTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()

    # * Create Client with agent
        self.client1 = Client.objects.create(
            name="Client1",
            email="client1@test.com",
            phone="123456789",
            notes="Notes",
            agent=self.agent_user,
        )

    # ! Test for Admin user creating a client
    def test_admin_user_create_client(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-list-create")
        data = {
            "name": "Client2",
            "email": "client2@test.com",
            "phone": "987654321",
            "notes": "Notes",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.get(id=response.data["id"]).agent, self.admin_user)

    # ! Test for Agent user creating a client
    def test_agent_user_create_client(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-list-create")
        data = {
            "name": "Client2",
            "email": "client2@test.com",
            "phone": "987654321",
            "notes": "Notes",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.get(id=response.data["id"]).agent, self.agent_user)

    # ! Test for Viewer trying to create a client
    def test_viewer_user_create_client(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-list-create")
        data = {
            "name": "Client2",
            "email": "client2@test.com",
            "phone": "987654321",
            "notes": "Notes",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user trying to create a client
    def test_unauthenticated_user_create_client(self):
        url = reverse("client-list-create")
        data = {
            "name": "Client2",
            "email": "client2@test.com",
            "phone": "987654321",
            "notes": "Notes",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # ! Test for Agent trying to create a client with existing email
    def test_agent_user_create_client_with_existing_email(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-list-create")
        data = {
            "name": "Client2",
            "email": self.client1.email,
            "phone": "987654321",
            "notes": "Notes",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


    # ! Test for trying to create a client with missing required fields
    def test_agent_user_create_client_with_missing_fields(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-list-create")
        data = {
            "name": "Client2",
            "phone": "987654321",
            "notes": "Notes",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        
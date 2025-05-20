from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from common_tests.base import BaseUserTestCase

class ClientsDeleteTests(BaseUserTestCase):
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

    # ! Test for Admin user deleting a client
    def test_admin_user_delete_client(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client1.id).exists())

    # ! Test for Agent user deleting a client
    def test_agent_user_delete_client(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client1.id).exists())
    
    # ! Test for Agent2 user trying to delete a client
    def test_agent2_user_delete_client(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Client.objects.filter(id=self.client1.id).exists())
    
    # ! Test for Viewer user trying to delete a client
    def test_viewer_user_delete_client(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("client-detail", args=[self.client1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Client.objects.filter(id=self.client1.id).exists())

    # ! Test for unauthenticated user trying to delete a client
    def test_unauthenticated_user_delete_client(self):
        url = reverse("client-detail", args=[self.client1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Client.objects.filter(id=self.client1.id).exists())
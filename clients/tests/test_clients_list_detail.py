from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from common_tests.base import BaseUserTestCase
class ClientsListDetailTests(BaseUserTestCase):
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

    # ! Test for Admin user accessing clients list
    def test_admin_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    # ! Test for agent user accessing clients list
    def test_agent_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    # ! Test for Agent2 user accessing clients list
    def test_agent2_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)

    # ! Test for Viewer user trying to access clients list
    def test_viewer_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user trying to access clients list
    def test_unauthenticated_user_access_clients_list(self):
        url = reverse("client-list-create")
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for Admin user accessing client detail
    def test_admin_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.data), 0)

    # ! Test for agent user accessing client detail
    def test_agent_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.data), 0)
    
    # ! Test for Agent2 user trying to access client detail
    def test_agent2_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ! Test for Viewer user trying to access client detail
    def test_viewer_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ! Test for unauthenticated user trying to access client detail
    def test_unauthenticated_user_access_client_detail(self):
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
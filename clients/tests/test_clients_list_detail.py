from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from rest_framework_simplejwt.tokens import RefreshToken

class ClientsListDetailTests(TestCase):
    def setUp(self):
        # * Create Admin User
        self.admin = CustomUser.objects.create_user(
            email="admin@test.com", password="admin123", role="admin"
        )

        # * Create Agent1 User
        self.agent1 = CustomUser.objects.create_user(
            email="agent1@test.com", password="agent123", role="agent"
        )

        # * Create Agent2 User
        self.agent2 = CustomUser.objects.create_user(
            email="agent2@test.com", password="agent123", role="agent"
        )

        # * Create Viewer User
        self.viewer = CustomUser.objects.create_user(
            email="viewer@test.com", password="viewer123", role="viewer"
        )

        # * Create Client with Agent1
        self.client1 = Client.objects.create(
            name="Cliente Uno",
            email="cliente1@test.com",
            phone="123456789",
            notes="Notas 1",
            agent=self.agent1,
        )

        # * Create APIClient instance
        self.api_client = APIClient()

    # ! Helper function to get JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    # ! Test for Admin user accessing clients list
    def test_admin_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.admin)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    # ! Test for Agent1 user accessing clients list
    def test_agent1_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.agent1)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)

    # ! Test for Agent2 user accessing clients list
    def test_agent2_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.agent2)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)

    # ! Test for Viewer user trying to access clients list
    def test_viewer_user_access_clients_list(self):
        jwt_token = self.get_jwt_token(self.viewer)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-list-create")
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user trying to access clients list
    def test_unauthenticated_user_access_clients_list(self):
        url = reverse("client-list-create")
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for Admin user accessing client detail
    def test_admin_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.admin)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.data), 0)

    # ! Test for Agent1 user accessing client detail
    def test_agent1_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.agent1)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertGreater(len(response.data), 0)
    
    # ! Test for Agent2 user trying to access client detail
    def test_agent2_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.agent2)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ! Test for Viewer user trying to access client detail
    def test_viewer_user_access_client_detail(self):
        jwt_token = self.get_jwt_token(self.viewer)
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
        
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # ! Test for unauthenticated user trying to access client detail
    def test_unauthenticated_user_access_client_detail(self):
        url = reverse("client-detail", args=[self.client1.id])
        
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
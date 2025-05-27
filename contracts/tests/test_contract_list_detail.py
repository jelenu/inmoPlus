from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from contracts.models import Contract
from common_tests.base import BaseUserTestCase
from properties.models import Property
from django.utils import timezone
from datetime import timedelta

class ContractsListDetailTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()

        # Create Agent2 User
        self.agent2_user = CustomUser.objects.create_user(
            email="agent2@test.com",
            password="agent2password123",
            first_name="Agent2",
            last_name="User",
            role="agent",
        )

        # Create Client with agent
        self.client1 = Client.objects.create(
            name="Client1",
            email="client1@test.com",
            phone="123456789",
            notes="Notes",
            agent=self.agent_user,
        )

        # Create a property for agent
        self.property = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent_user,
        )

        # Create a contract for the property
        self.contract =Contract.objects.create(
            property=self.property,
            client=self.client1,
            agent=self.agent_user,
            type='rental',
            price=1000.00,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            document=None,
        )

    # ! Test for Admin user listing contracts
    def test_admin_user_list_contracts(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ! Test for Agent user listing contracts
    def test_agent_user_list_contracts(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ! Test for Agent2 user listing contracts
    def test_agent2_user_list_contracts(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # !Test for viewer user listing contracts
    def test_viewer_user_list_contracts(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user listing contracts
    def test_unauthenticated_user_list_contracts(self):
        url = reverse("contract-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  


    # ! Test for Admin user retrieving a contract
    def test_admin_user_retrieve_contract(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.contract.id)

    # ! Test for Agent user retrieving a contract
    def test_agent_user_retrieve_contract(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.contract.id)

    # ! Test for Agent2 user retrieving a contract
    def test_agent2_user_retrieve_contract(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  

    # ! Test for viewer user retrieving a contract
    def test_viewer_user_retrieve_contract(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
    
    # ! Test for unauthenticated user retrieving a contract
    def test_unauthenticated_user_retrieve_contract(self):
        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
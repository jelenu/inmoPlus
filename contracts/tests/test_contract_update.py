from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from clients.models import Client
from contracts.models import Contract
from common_tests.base import BaseUserTestCase
from properties.models import Property
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

class ContractUpdateTests(BaseUserTestCase):
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

    # ! Test for admin user updating a contract
    def test_admin_user_update_contract(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "price": 1200.00,

        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.price, 1200.00)

    # ! Test for agent user updating a contract
    def test_agent_user_update_contract(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "price": 1200.00,
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.price, 1200.00)

    # ! Test for agent2 user trying to update a contract
    def test_agent2_user_update_contract(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "price": 1200.00,
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.contract.refresh_from_db()
        self.assertNotEqual(self.contract.price, 1200.00)

    # ! Test for viewer user trying to update a contract
    def test_viewer_user_update_contract(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "price": 1200.00,
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.contract.refresh_from_db()
        self.assertNotEqual(self.contract.price, 1200.00)

    # ! Test for unauthenticated user trying to update a contract
    def test_unauthenticated_user_update_contract(self):
        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "price": 1200.00,
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.contract.refresh_from_db()
        self.assertNotEqual(self.contract.price, 1200.00)

    # ! Test for updating contract with invalid start date
    def test_update_contract_with_invalid_start_date(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "start_date": timezone.now().date() + timedelta(days=31),
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # ! Test for updating contract with invalid end date
    def test_update_contract_with_invalid_end_date(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "end_date": timezone.now().date() - timedelta(days=1),
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("End date cannot be before start date.", response.data['end_date'])

    # ! Test for updating contract with a signed status
    def test_update_contract_to_signed_status(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-detail", kwargs={"pk": self.contract.id})
        updated_data = {
            "status": "signed",
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.status, "signed")
        self.assertEqual(self.contract.property.status, "rented")
    

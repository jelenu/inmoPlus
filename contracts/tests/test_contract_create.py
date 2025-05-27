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

class ContractsCreateTests(BaseUserTestCase):
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

    # ! Test for Agent creating a contract
    def test_agent_create_contract(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=response.data['id'])
        self.assertEqual(contract.property, self.property)
        self.assertEqual(contract.client, self.client1)
        self.assertEqual(contract.agent, self.agent_user)

    # ! Test for admin creating a contract
    def test_admin_create_contract(self):
        jwt_token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "sale",
            "price": 200000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=60),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contract = Contract.objects.get(id=response.data['id'])
        self.assertEqual(contract.property, self.property)
        self.assertEqual(contract.client, self.client1)
        self.assertEqual(contract.agent, self.admin_user)

    # ! Test for Agent2 trying to create a contract
    def test_agent2_create_contract(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You can only create contracts for your own properties.", str(response.data))

    # ! Test for viewer user trying to create a contract
    def test_viewer_create_contract(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ! Test for unauthenticated user trying to create a contract
    def test_unauthenticated_create_contract(self):
        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for creating a contract with invalid end date
    def test_create_contract_with_invalid_end_date(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() - timedelta(days=1),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("End date cannot be before start date.", str(response.data))
    
    # ! Test for creating a contract with unavailable property
    def test_create_contract_with_unavailable_property(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        # Change property status to unavailable
        self.property.status = 'unavailable'
        self.property.save()

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Property must be available to create a contract.", str(response.data))

    # ! Test for creating a contract when a signed contract already exists for the property
    def test_create_contract_with_signed_contract_exists(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        # Create a signed contract for the property
        Contract.objects.create(
            property=self.property,
            client=self.client1,
            agent=self.agent_user,
            type='rental',
            price=1000.00,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            document=None,
            status='signed'
        )

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("There is already a signed contract for this property.", str(response.data))

    # ! Test for creating a contract with a property not owned by the agent
    def test_create_contract_with_property_not_owned_by_agent(self):
        jwt_token = self.get_jwt_token(self.agent2_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("contract-list-create")
        data = {
            "property": self.property.id,
            "client": self.client1.id,
            "type": "rental",
            "price": 1000.00,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=30),
            "document": SimpleUploadedFile("test_doc.pdf", b"dummy content", content_type="application/pdf"),
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You can only create contracts for your own properties.", str(response.data))
    

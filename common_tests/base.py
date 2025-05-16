from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class BaseUserTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # * Create viewer user
        self.viewer_user = CustomUser.objects.create_user(
            email="vieweruser@test.com",
            password="viewerpassword123",
            first_name="Viewer",
            last_name="User",
            role="viewer",
        )

        # * Create agent user
        self.agent_user = CustomUser.objects.create_user(
            email="agentuser@test.com",
            password="agentpassword123",
            first_name="Agent",
            last_name="User",
            role="agent",
        )

         # * Create admin user
        self.admin_user = CustomUser.objects.create_user(
            email="admin@test.com",
            password="adminpassword123",
            first_name="Admin",
            last_name="User",
            role="admin",
        )
        
        # * APIClient instance
        self.client = APIClient()

    # ! Helper function to get JWT token
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

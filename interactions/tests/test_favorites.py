from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from common_tests.base import BaseUserTestCase
from interactions.models import Favorite
from properties.models import Property

class FavoritesTests(BaseUserTestCase):
    def setUp(self):
        super().setUp()

        # * Create viewer user
        self.viewer_user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User",
        )
        # * Create property
        self.property = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent_user,
        )

        # * Create property 2
        self.property2 = Property.objects.create(
            title="Property 1",
            description="Property 1 Description",
            price=100000,
            address="123 Property Street",
            owner=self.agent_user,
        )

        # * add propery to favorites
        Favorite.objects.create(user=self.viewer_user, property=self.property)

    # ! Test for viewer user adding a property to favorites
    def test_viewer_user_add_favorite(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("favorite-toggle", args=[self.property2.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Favorite.objects.count(), 2)
        self.assertEqual(Favorite.objects.first().property, self.property)

    # ! Test for viewer user removing a property from favorites
    def test_viewer_user_remove_favorite(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("favorite-toggle", args=[self.property.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Favorite.objects.count(), 0)

    # ! Test for viewer user listing favorites
    def test_viewer_user_list_favorites(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("favorite-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ! Test for viewer user trying to favorite a non-existent property
    def test_viewer_user_favorite_non_existent_property(self):
        jwt_token = self.get_jwt_token(self.viewer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("favorite-toggle", args=[9999])  # Non-existent property ID
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Favorite.objects.count(), 1)

    # ! Test for unauthenticated user trying to list favorites
    def test_unauthenticated_user_list_favorites(self):
        url = reverse("favorite-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ! Test for unauthenticated user trying to add a favorite
    def test_unauthenticated_user_add_favorite(self):
        url = reverse("favorite-toggle", args=[self.property.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Favorite.objects.count(), 1)

    # ! Test for agent user trying to add a favorite
    def test_agent_user_add_favorite(self):
        jwt_token = self.get_jwt_token(self.agent_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

        url = reverse("favorite-toggle", args=[self.property2.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Favorite.objects.count(), 1)

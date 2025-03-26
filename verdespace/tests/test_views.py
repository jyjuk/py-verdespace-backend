from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from verdespace.models import Plant, Comment, WishList

User = get_user_model()


class PlantViewSetTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password123"
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.plant = Plant.objects.create(
            name="Spider Plant",
            description="A test description",
            tips="Water once a week",
            light_needs="Indirect light",
            water_needs="Moderate",
            care="Easy",
            air_purifying=True,
            allergenic=False,
            size="Small",
            blooms=False,
            category="Air-Purifying",
        )

    def test_list_plants_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/verdespace/plants/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_plants_as_unauthenticated_user(self):
        response = self.client.get("/api/verdespace/plants/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_plant_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            "name": "New Plant",
            "description": "Another test description",
            "tips": "Keep soil moist",
            "light_needs": "Full sun",
            "water_needs": "High",
            "care": "Medium",
            "air_purifying": False,
            "allergenic": True,
            "size": "Medium",
            "blooms": True,
            "category": "Flowering",
        }
        response = self.client.post("/api/verdespace/plants/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Plant.objects.count(), 2)

    def test_create_plant_as_non_superuser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Another Plant",
            "description": "Another test description",
            "tips": "Keep in shade",
            "light_needs": "Low light",
            "water_needs": "Low",
            "care": "Easy",
            "air_purifying": True,
            "allergenic": False,
            "size": "Small",
            "blooms": False,
            "category": "Decorative",
        }
        response = self.client.post("/api/verdespace/plants/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.plant = Plant.objects.create(
            name="Cactus",
            description="A test cactus",
            tips="Keep in full sun",
            light_needs="Full sun",
            water_needs="Low",
            care="Easy",
            air_purifying=False,
            allergenic=True,
            size="Small",
            blooms=True,
            category="Cactus",
        )
        self.comment = Comment.objects.create(
            text="This is a test comment",
            author=self.user,
            plant=self.plant,
        )

    def test_list_comments(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/verdespace/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_comment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "text": "Another comment",
            "plant": self.plant.id,
        }  # Передаємо поле "plant"
        response = self.client.post("/api/verdespace/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_create_comment_as_unauthenticated_user(self):
        data = {"text": "Another comment", "plant": self.plant.id}
        response = self.client.post("/api/verdespace/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WishListViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.plant = Plant.objects.create(
            name="Aloe Vera",
            description="A test aloe vera",
            tips="Keep in bright indirect light",
            light_needs="Bright, indirect",
            water_needs="Moderate",
            care="Medium",
            air_purifying=True,
            allergenic=False,
            size="Medium",
            blooms=True,
            category="Medicinal",
        )
        self.wishlist = WishList.objects.create(user=self.user, plant=self.plant)

    def test_list_wishlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/verdespace/wishlists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_to_wishlist(self):
        self.client.force_authenticate(user=self.user)
        new_plant = Plant.objects.create(
            name="Test Plant",
            description="Test description",
            tips="Test tips",
            light_needs="Low light",
            water_needs="Low",
            care="Easy",
            air_purifying=False,
            allergenic=False,
            size="Small",
            blooms=False,
            category="Air-Purifying",
        )
        data = {"plant_id": new_plant.id}
        response = self.client.post("/api/verdespace/wishlists/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishList.objects.count(), 2)

    def test_duplicate_wishlist_entry(self):
        self.client.force_authenticate(user=self.user)
        data = {"plant_id": self.plant.id}
        response = self.client.post("/api/verdespace/wishlists/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

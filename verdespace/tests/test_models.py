from django.test import TestCase
from django.contrib.auth import get_user_model
from verdespace.models import Plant, Comment, WishList

User = get_user_model()


class PlantModelTest(TestCase):
    def setUp(self):
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

    def test_plant_creation(self):
        self.assertEqual(self.plant.name, "Spider Plant")
        self.assertTrue(self.plant.air_purifying)
        self.assertFalse(self.plant.blooms)

    def test_str_representation(self):
        self.assertEqual(str(self.plant), "Spider Plant")


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password"
        )
        self.plant = Plant.objects.create(
            name="Aloe Vera",
            description="Medicinal plant",
            tips="Keep near sunlight",
            light_needs="Bright, direct",
            water_needs="Low",
            care="Easy",
            air_purifying=False,
            allergenic=False,
            size="Medium",
            blooms=True,
            category="Medicinal",
        )
        self.comment = Comment.objects.create(
            text="This is a test comment",
            author=self.user,
            plant=self.plant,
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, "This is a test comment")
        self.assertEqual(self.comment.author.username, "testuser")
        self.assertEqual(self.comment.plant.name, "Aloe Vera")


class WishListModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password"
        )
        self.plant = Plant.objects.create(
            name="Cactus",
            description="A test description",
            tips="Keep in full sun",
            light_needs="Full sun",
            water_needs="Low",
            care="Easy",
            air_purifying=False,
            allergenic=False,
            size="Small",
            blooms=True,
            category="Cactus",
        )
        self.wishlist = WishList.objects.create(user=self.user, plant=self.plant)

    def test_wishlist_creation(self):
        self.assertEqual(self.wishlist.user.username, "testuser")
        self.assertEqual(self.wishlist.plant.name, "Cactus")

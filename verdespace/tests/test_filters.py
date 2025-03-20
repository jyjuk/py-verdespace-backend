from django.test import TestCase
from django_filters import FilterSet
from verdespace.models import Plant
from verdespace.filters import PlantFilter


class PlantFilterTest(TestCase):
    def setUp(self):
        self.plant1 = Plant.objects.create(
            name="Spider Plant",
            description="A test description",
            tips="Keep near sunlight",
            light_needs="Indirect light",
            water_needs="Moderate",
            care="Easy",
            air_purifying=True,
            allergenic=False,
            size="Small",
            blooms=False,
            category="Air-Purifying",
        )
        self.plant2 = Plant.objects.create(
            name="Cactus",
            description="Thorny plant",
            tips="Low maintenance",
            light_needs="Full sun",
            water_needs="Low",
            care="Easy",
            air_purifying=False,
            allergenic=True,
            size="Medium",
            blooms=True,
            category="Cactus",
        )

    def test_filter_by_name(self):
        filterset = PlantFilter({"name": "Spider"}, queryset=Plant.objects.all())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().name, "Spider Plant")

    def test_filter_by_air_purifying(self):
        filterset = PlantFilter({"air_purifying": "true"}, queryset=Plant.objects.all())
        self.assertEqual(filterset.qs.count(), 1)
        self.assertTrue(filterset.qs.first().air_purifying)

from django.core.management import call_command
from django.test import TestCase
from verdespace.models import Plant


class FixtureTest(TestCase):
    def test_loaddata(self):
        call_command("loaddata", "plantsdata_cleaned.json")
        self.assertEqual(Plant.objects.count(), 100)

    def test_loaded_data_content(self):
        call_command("loaddata", "plantsdata_cleaned.json")
        plant = Plant.objects.first()
        self.assertEqual(plant.name, "Spider Plant")  # Очікуване значення

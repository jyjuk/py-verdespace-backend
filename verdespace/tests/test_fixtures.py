from django.core.management import call_command
from django.test import TestCase
from verdespace.models import Plant


class FixtureTest(TestCase):
    def test_loaddata(self):
        call_command("loaddata", "plantsdata_converted.json")
        self.assertEqual(Plant.objects.count(), 100)

from django_filters import rest_framework as filters
from .models import Plant


class PlantFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains", label="Name of the plant")
    size = filters.ChoiceFilter(choices=Plant.SIZE_CHOICES, label="Plant size")
    blooms = filters.BooleanFilter(label="Does the plant bloom?")
    water_needs = filters.ChoiceFilter(
        choices=Plant.WATER_REQUIREMENT_CHOICES, label="Water needs"
    )
    light_needs = filters.ChoiceFilter(
        choices=Plant.SUNLIGHT_REQUIREMENT_CHOICES, label="Light needs"
    )
    allergenic = filters.BooleanFilter(label="Is the plant allergenic?")
    air_purifying = filters.BooleanFilter(label="Is the plant air-purifying?")
    category = filters.ChoiceFilter(choices=Plant.CATEGORY_CHOICES, label="Category")

    class Meta:
        model = Plant
        fields = [
            "name",
            "size",
            "blooms",
            "water_needs",
            "light_needs",
            "allergenic",
            "air_purifying",
            "category",
        ]

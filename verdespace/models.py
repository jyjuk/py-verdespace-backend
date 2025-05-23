from django.conf import settings
from django.db import models
import uuid


class Plant(models.Model):
    SIZE_CHOICES = [
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large"),
    ]

    WATER_REQUIREMENT_CHOICES = [
        ("Rarely", "Rarely"),
        ("Moderately", "Moderately"),
        ("Often", "Often"),
    ]

    SUNLIGHT_REQUIREMENT_CHOICES = [
        ("Bright", "Bright"),
        ("Scattered", "Scattered"),
        ("Shadow", "Shadow"),
    ]

    CARE_REQUIREMENT_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Difficult", "Difficult"),
    ]

    CATEGORY_CHOICES = [
        ("Air-Purifying", "Air-Purifying"),
        ("Decorative", "Decorative"),
        ("Flowering", "Flowering"),
        ("Succulent", "Succulent"),
        ("Cactus", "Cactus"),
        ("Rare", "Rare"),
        ("Edible", "Edible"),
        ("Medicinal", "Medicinal"),
        ("Climbing", "Climbing"),
        ("Ornamental Grass", "Ornamental Grass"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    tips = models.TextField()
    light_needs = models.CharField(max_length=10, choices=SUNLIGHT_REQUIREMENT_CHOICES)
    water_needs = models.CharField(max_length=15, choices=WATER_REQUIREMENT_CHOICES)
    care = models.CharField(max_length=10, choices=CARE_REQUIREMENT_CHOICES)
    air_purifying = models.BooleanField(default=False)
    allergenic = models.BooleanField(default=False)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    blooms = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def average_rating(self):
        ratings = self.ratings.all()
        return round(sum(r.rating for r in ratings) / len(ratings), 2) if ratings else None

    def __str__(self):
        return self.name


def unique_image_name(instance, filename):
    """
    Генерує унікальну назву для зображення.
    """
    extension = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return f"plants/{unique_filename}"


class PlantImage(models.Model):
    plant = models.ForeignKey("Plant", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=unique_image_name
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.plant.name}"


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(
        "Plant", related_name="comments", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="comments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent:
            return f"Reply by {self.author} to {self.parent.author}'s comment"
        return f"Comment by {self.author} on {self.plant}"


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(
        Plant, related_name="wishlists", on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.plant.name if self.plant else 'No plant specified'}"


class Rating(models.Model):
    plant = models.ForeignKey(Plant, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ('plant', 'user')  # Кожен користувач може оцінити рослину лише один раз

    def __str__(self):
        return f"Rating {self.rating} by {self.user} for {self.plant}"

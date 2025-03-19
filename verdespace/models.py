from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Plant(models.Model):
    SIZE_CHOICES = [
        ('Extra Small', 'Extra Small'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Extra Large', 'Extra Large'),
    ]

    WATER_REQUIREMENT_CHOICES = [
        ('Very Low', 'Very Low'),
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High'),
        ('Very High', 'Very High')
    ]

    SUNLIGHT_REQUIREMENT_CHOICES = [
        ('Indirect light', 'Indirect light'),
        ('Low to medium', 'Low to medium'),
        ('Bright, indirect', 'Bright, indirect'),
        ('Low to bright', 'Low to bright'),
        ('Bright, direct', 'Bright, direct'),
        ('Filtered light', 'Filtered light'),
        ('Full sun', 'Full sun'),
        ('Full shade', 'Full shade'),
        ('Medium, indirect', 'Medium, indirect'),
        ('Bright light with some direct sun', 'Bright light with some direct sun'),
    ]

    CARE_REQUIREMENT_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Difficult', 'Difficult'),
    ]

    CATEGORY_CHOICES = [
        ('Air-Purifying', 'Air-Purifying'),
        ('Decorative', 'Decorative'),
        ('Flowering', 'Flowering'),
        ('Succulent', 'Succulent'),
        ('Cactus', 'Cactus'),
        ('Rare', 'Rare'),
        ('Edible', 'Edible'),
        ('Medicinal', 'Medicinal'),
        ('Climbing', 'Climbing'),
        ('Ornamental Grass', 'Ornamental Grass'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    tips = models.TextField()
    light_needs = models.CharField(max_length=35, choices=SUNLIGHT_REQUIREMENT_CHOICES)
    water_needs = models.CharField(max_length=10, choices=WATER_REQUIREMENT_CHOICES)
    care = models.CharField(max_length=10, choices=CARE_REQUIREMENT_CHOICES)
    air_purifying = models.BooleanField(default=False)
    allergenic = models.BooleanField(default=False)
    size = models.CharField(max_length=15, choices=SIZE_CHOICES)
    blooms = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.plant}'


class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, related_name="wishlists", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.plant.name}"


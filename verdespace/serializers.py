from rest_framework import serializers
from .models import Plant, Comment, WishList


class PlantSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ["id", "name", "image", "description"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "created_at"]


class WishListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    plant = PlantSummarySerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(), write_only=True
    )

    class Meta:
        model = WishList
        fields = ["id", "user", "plant", "plant_id", "created_at"]

    def create(self, validated_data):
        plant = validated_data.pop("plant_id")
        user = self.context["request"].user
        if WishList.objects.filter(user=user, plant=plant).exists():
            raise serializers.ValidationError("This plant is already in your wishlist.")
        return WishList.objects.create(user=user, plant=plant)


class PlantDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"

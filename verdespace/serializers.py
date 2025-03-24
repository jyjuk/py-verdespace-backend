from rest_framework import serializers
from .models import Plant, Comment, WishList, PlantImage


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ["id", "image"]


class PlantSummarySerializer(serializers.ModelSerializer):
    images = PlantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ["id", "name", "images", "description"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "text", "plant", "author", "parent", "replies", "image", "created_at"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


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
    images = PlantImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = "__all__"

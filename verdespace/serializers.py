from rest_framework import serializers
from .models import Plant, Comment, WishList, PlantImage, Rating


class PlantImageSerializer(serializers.ModelSerializer):
    """
    Serializer for PlantImage model to handle image data.
    """

    class Meta:
        model = PlantImage
        fields = ["id", "image", "plant", "uploaded_at"]

    def get_image_url(self, obj):
        """
        Generate the public URL for the image.
        """
        return obj.image.url


class PlantSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for summarized plant information.
    """

    images = PlantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ["id", "name", "images", "description"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """

    author = serializers.ReadOnlyField(source="author.username")
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all())
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), required=False, allow_null=True
    )
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "plant",
            "author",
            "parent",
            "replies",
            "image",
            "created_at",
        ]

    def get_replies(self, obj):
        """
        Retrieve replies for the current comment.
        Limit number of replies for performance.
        """
        return CommentSerializer(
            obj.replies.all()[:10], many=True
        ).data  # Ліміт на 10 відповідей


class WishListSerializer(serializers.ModelSerializer):
    """
    Serializer for the WishList model.
    """

    user = serializers.ReadOnlyField(source="user.username")
    plant = PlantSummarySerializer(read_only=True)
    plant_id = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all(), write_only=True
    )

    class Meta:
        model = WishList
        fields = ["id", "user", "plant", "plant_id", "created_at"]

    def create(self, validated_data):
        """
        Create a new WishList entry.
        Ensure the plant isn't already in the wishlist.
        """
        plant = validated_data.pop("plant_id")
        user = self.context["request"].user
        if WishList.objects.filter(user=user, plant=plant).exists():
            raise serializers.ValidationError("This plant is already in your wishlist.")
        return WishList.objects.create(user=user, plant=plant)


class PlantDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the Plant model.
    """

    images = PlantImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = [
            "id",
            "name",
            "description",
            "tips",  # Додано поле "tips", якщо воно потрібне
            "size",
            "light_needs",
            "water_needs",
            "care",
            "air_purifying",
            "allergenic",
            "blooms",
            "category",
            "images",
            "comments",
            "created_at",
            "average_rating",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['plant', 'user', 'rating']

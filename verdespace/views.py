from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Plant, Comment, WishList, PlantImage
from .serializers import (
    PlantSummarySerializer,
    PlantDetailSerializer,
    CommentSerializer,
    WishListSerializer,
    PlantImageSerializer,
)
from .telegram_sender import telegram_sender
from .utils import generate_presigned_url


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow only admin users to modify data
    and others to have read-only access.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow only the author of an object to modify it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a summary of all plants with their images"
    ),
    retrieve=extend_schema(
        description="Retrieve detailed information about a specific plant, including images"
    ),
    create=extend_schema(description="Create a new plant (only for staff users)"),
)
class PlantViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Plant model.
    Includes custom actions for uploading and retrieving images.
    """

    queryset = Plant.objects.prefetch_related("images", "comments")
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        Return the appropriate serializer based on the action.
        """
        if self.action == "list":
            return PlantSummarySerializer
        return PlantDetailSerializer

    @staticmethod
    def notify_b(plant):
        """
        Send a Telegram notification about the creation of a new plant.
        """
        message = (
            f"New Plant Added\n"
            f"Plant ID: {plant.pk}\n"
            f"Plant Name: {plant.name}\n"
            f"Plant Size: {plant.size}\n"
        )
        try:
            telegram_sender.send_message(message)
        except Exception as e:
            print(f"Error sending notification: {e}")

    def perform_create(self, serializer):
        """
        Save the new plant and send a notification.
        """
        plant = serializer.save()
        self.notify_b(plant)

    @action(detail=True, methods=["post"], url_path="images")
    def upload_image(self, request, pk=None):
        """
        Custom action to handle uploading images for a plant.
        - POST: Upload a new image for the plant.
        """
        plant = self.get_object()
        image = request.FILES.get("image")

        if not image:
            return Response(
                {"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        if image.size > 5 * 1024 * 1024:  # Limit: 5MB
            return Response(
                {"error": "Image too large"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not image.content_type.startswith("image/"):
            return Response(
                {"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST
            )

        PlantImage.objects.create(plant=plant, image=image)
        return Response(
            {"status": "Image uploaded successfully"}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["get"], url_path="images")
    def retrieve_images(self, request, pk=None):
        """
        Custom action to retrieve all images for a plant.
        - GET: Retrieve all images associated with the plant.
        """
        plant = self.get_object()
        images = plant.images.all()
        serializer = PlantImageSerializer(images, many=True)

        for image in serializer.data:
            image_key = image.get("image")
            image["pre_signed_url"] = generate_presigned_url(image_key)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="generate-image-url")
    def generate_image_url(self, request, pk=None):
        """
        Generate a Pre-signed URL for a specific plant image.
        """
        plant = self.get_object()
        if not plant.images.exists():
            return Response(
                {"error": "No images available"}, status=status.HTTP_404_NOT_FOUND
            )

        image_key = plant.images.first().image.name  # Get the first image's key
        url = generate_presigned_url(image_key)
        if url:
            return Response({"url": url})
        return Response(
            {"error": "Failed to generate URL"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for Comment model.
    """

    queryset = Comment.objects.select_related("author", "plant", "parent")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Set the author of the comment to the current user.
        """
        serializer.save(author=self.request.user)


@extend_schema_view(
    retrieve=extend_schema(
        parameters=[
            {
                "name": "id",
                "type": "integer",
                "required": True,
                "description": "ID of the wishlist item",
                "in": "path",
            }
        ]
    )
)
class WishListViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for WishList model.
    """

    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        """
        Return the wishlist items for the current user.
        """
        return WishList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Ensure that a plant is only added to the wishlist once.
        """
        plant = serializer.validated_data.get("plant_id")
        wishlist, created = WishList.objects.get_or_create(
            user=self.request.user, plant=plant
        )
        if not created:
            raise serializers.ValidationError("This plant is already in your wishlist.")
        return wishlist


class PlantImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle CRUD operations for PlantImage model.
    """

    queryset = PlantImage.objects.select_related("plant")
    serializer_class = PlantImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new image for a plant.
        """
        serializer.save()

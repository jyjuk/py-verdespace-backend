from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions, serializers
from django_filters.rest_framework import DjangoFilterBackend
from .models import Plant, Comment, WishList
from .serializers import (
    PlantSummarySerializer,
    PlantDetailSerializer,
    CommentSerializer,
    WishListSerializer,
)
from .filters import PlantFilter
from .telegram_sender import telegram_sender


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):
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
    create=extend_schema(
        description="Create a new plant (only for staff users)"
    ),
)
class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.prefetch_related("images")
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = PlantFilter

    def get_serializer_class(self):
        if self.action == "list":
            return PlantSummarySerializer
        return PlantDetailSerializer

    @staticmethod
    def notify_b(plant):
        message = (
            f"New Plant Added \n"
            f"Plant ID: {plant.pk}\n"
            f"Plant Name: {plant.name}\n"
            f"Plant Size: {plant.size}\n"
        )
        try:
            telegram_sender.send_message(message)
        except Exception as e:
            print(f"Error sending notification: {e}")

    def perform_create(self, serializer):
        plant = serializer.save()
        self.notify_b(plant)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'plant', 'parent')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
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
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        plant = serializer.validated_data.get("plant_id")
        wishlist, created = WishList.objects.get_or_create(user=self.request.user, plant=plant)
        if not created:
            raise serializers.ValidationError("This plant is already in your wishlist.")
        return wishlist

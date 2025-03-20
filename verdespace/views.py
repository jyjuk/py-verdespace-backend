from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions
from .models import Plant, Comment, WishList
from .serializers import (
    PlantSummarySerializer,
    PlantDetailSerializer,
    CommentSerializer,
    WishListSerializer,
)
from rest_framework import serializers

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


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return PlantSummarySerializer
        return PlantDetailSerializer

    @staticmethod
    def notify_b(plant):
        message = (
            f"New Plant Created \n"
            f"Plant ID: {plant.pk}\n"
            f"Plant Name: {plant.name}\n"
            f"Plant Size: {plant.size}\n"
        )
        telegram_sender.send_message(message)

    def perform_create(self, serializer):
        plant = serializer.save()
        self.notify_b(plant)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        plant_id = self.request.query_params.get("plant")
        if plant_id:
            return Comment.objects.filter(plant_id=plant_id)
        return super().get_queryset()

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
        plant = serializer.validated_data.get("plant")
        if WishList.objects.filter(user=self.request.user, plant=plant).exists():
            raise serializers.ValidationError("This plant is already in your wishlist.")
        serializer.save(user=self.request.user)

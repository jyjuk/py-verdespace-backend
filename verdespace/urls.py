from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, CommentViewSet, WishListViewSet, PlantImageViewSet

router = DefaultRouter()
router.register(r"plants", PlantViewSet, basename="plants")
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r"wishlists", WishListViewSet, basename="wishlists")
router.register(r"plant-images", PlantImageViewSet, basename="plant-images")

urlpatterns = [
    path("", include(router.urls)),
]
app_name = "verdespace"

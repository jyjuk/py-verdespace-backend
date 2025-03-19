from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, CommentViewSet, WishListViewSet

router = DefaultRouter()
router.register(r"plants", PlantViewSet, basename="plants")
router.register(r"comments", CommentViewSet, basename="comments")
router.register(r"wishlists", WishListViewSet, basename="wishlists")
urlpatterns = [
    path("", include(router.urls)),
    path("wishlists/<int:id>/", WishListViewSet.as_view({"get": "retrieve"})),
]
app_name = "verdespace"

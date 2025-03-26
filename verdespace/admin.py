from django.contrib import admin
from django.db.models import Count
from .models import Plant, Comment, WishList
from .models import PlantImage


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "size",
        "care",
        "air_purifying",
        "blooms",
        "comments_count",
    )
    search_fields = ("name", "description")
    list_filter = ("category", "light_needs", "water_needs")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(comments_count=Count("comments"))

    def comments_count(self, obj):
        return obj.comments_count

    comments_count.admin_order_field = "comments_count"
    comments_count.short_description = "Number of Comments"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "plant", "created_at", "short_text")
    search_fields = ("text",)
    list_filter = ("author", "plant")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author", "plant")

    def short_text(self, obj):
        return obj.text[:50]

    short_text.short_description = "Comment Text"


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("user", "plant", "created_at")
    search_fields = ("user__username", "plant__name")
    list_filter = ("user",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "plant")


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ["plant", "image"]

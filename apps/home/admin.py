
from django.contrib import admin
from .models import RunningClub, RunPost


@admin.register(RunningClub)
class RunningClubAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(RunPost)
class RunPostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "club",
        "created_by",
        "run_type",
        "date",
        "start_time",
        "target_pace",
        "route_distance_km",
        "max_runners",
    )

    list_filter = ("date", "run_type", "club")

    search_fields = (
        "title",
        "description",
        "venue_name",
        "club__name",
        "created_by__username",
    )

    readonly_fields = ("created_at",)

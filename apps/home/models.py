from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RunningClub(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo_url = models.URLField(
        blank=True, 
        null=True,
        help_text="URL to club avatar image"
    )
    avatar_Bg = models.CharField(
        max_length=20, 
        default="bg-rose-700",
        help_text="Tailwind fallback color if no logo is uploaded"
    )
    city = models.CharField(max_length=100, default="Cebu City")

    def __str__(self):
        return self.name

    @property
    def initials(self):
        words = self.name.split()
        return "".join(w[0] for w in words[:2]).upper()


class RunPost(models.Model):
    RUN_TYPE_CHOICES = [
        ("Social", "Social"),
        ("Training", "Training"),
        ("Tempo", "Tempo"),
        ("Long Run", "Long Run"),
        ("Intervals", "Intervals"),
        ("Race", "Race"),
    ]

    club = models.ForeignKey(
        RunningClub, 
        on_delete=models.CASCADE, 
        related_name="run_posts"
    )
    title = models.CharField(max_length=140)
    run_type = models.CharField(
        max_length=20, 
        choices=RUN_TYPE_CHOICES, 
        default="Social"
    )
    venue_name = models.CharField(max_length=120)
    
    # Running-specific metrics
    route_distance_km = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        help_text="Run distance or distance from user in km (e.g. 5.0)"
    )
    target_pace = models.CharField(
        max_length=30, 
        default="6:00/km", 
        help_text="e.g., 5:30/km or Easy Pace"
    )

    # Schedule & Capacity
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    max_runners = models.PositiveIntegerField(default=20)
    participants = models.ManyToManyField(
        User, 
        related_name="joined_runs", 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.club.name})"

    @property
    def spots_taken(self):
        return self.participants.count()

    @property
    def is_full(self):
        return self.spots_taken >= self.max_runners
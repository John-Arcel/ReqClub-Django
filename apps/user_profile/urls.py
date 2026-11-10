from django.urls import path
from .views import profile_view

app_name = "user_profile"

# Make sure this is spelled exactly 'urlpatterns'
urlpatterns = [
    path("", profile_view, name="profile"),
]
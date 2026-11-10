from django.urls import path
from .views import settings_view

# Namespace perfectly updated to user_setting
app_name = "user_setting"

urlpatterns = [
    path("", settings_view, name="settings"),
]
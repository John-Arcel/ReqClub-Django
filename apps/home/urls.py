from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home_dashboard, name="home"),
    path("runs/<int:run_id>/toggle-join/", views.toggle_join_run, name="toggle_join_run"),
]
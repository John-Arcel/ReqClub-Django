from django.shortcuts import render, redirect
from .models import UserSettings 

def settings_view(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == "POST":
        settings.dark_mode = request.POST.get("dark_mode") == "on"
        settings.email_notifications = request.POST.get("email_notifications") == "on"
        
        settings.save()
        
        # Redirect perfectly updated to user_setting
        return redirect("user_setting:settings")

    # Render path perfectly updated to user_setting
    return render(request, "user_setting/settings.html", {"settings": settings})
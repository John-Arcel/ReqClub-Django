from django.shortcuts import render, redirect
from .models import Profile

def profile_view(request):
    # Safely gets the profile or creates a blank one if the user just registered
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name", "")
        profile.bio = request.POST.get("bio", "")
        
        # This specifically handles the image upload
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
            
        profile.save()
        return redirect("user_profile:profile")

    return render(request, "user_profile/profile.html", {"profile": profile})
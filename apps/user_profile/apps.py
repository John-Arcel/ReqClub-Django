from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # CRITICAL: This tells Django exactly where the app lives
    name = 'apps.user_profile'
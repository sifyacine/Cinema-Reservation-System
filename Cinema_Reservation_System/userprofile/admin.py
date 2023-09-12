from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Add any additional fields you want to display in the list view
    # Add any other customizations to the admin panel for UserProfile model
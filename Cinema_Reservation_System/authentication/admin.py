# authentication/admin.py

from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    
    list_display = ['first_name', 'last_name', 'email', 'phone_number']

    search_fields = ['first_name', 'last_name', 'email', 'phone_number']


# Register the UserProfile model with the custom admin class
admin.site.register(UserProfile, UserProfileAdmin)

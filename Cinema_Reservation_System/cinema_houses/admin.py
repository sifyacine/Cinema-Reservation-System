# cinema/admin.py

from django.contrib import admin
from .models import Cinema, Showtime

class ShowtimeInline(admin.TabularInline):
    model = Showtime
    extra = 1

class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email_contact', 'rating', 'phone_number')
    search_fields = ('name', 'address')
    list_filter = ('rating',)
    inlines = [ShowtimeInline]  # Add the ShowtimeInline to the CinemaAdmin only

admin.site.register(Cinema, CinemaAdmin)

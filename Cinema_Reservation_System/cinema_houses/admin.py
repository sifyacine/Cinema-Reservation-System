from django.contrib import admin
from cinema_houses.models import Showtime, CinemaHouse


class CinemaHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating')
    list_filter = ('location', 'rating')
    search_fields = ('name', 'location')


class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'display_cinema_houses', 'date', 'time', 'is_available')
    list_filter = ('date', 'is_available')

    def display_cinema_houses(self, obj):
        return ', '.join([cinema.name for cinema in obj.cinema_houses.all()])

    display_cinema_houses.short_description = 'Cinema Houses'

admin.site.register(CinemaHouse)
admin.site.register(Showtime, ShowtimeAdmin)

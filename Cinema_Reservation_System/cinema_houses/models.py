from django.db import models

class CinemaHouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie_title = models.CharField(max_length=255)  # Movie title from IMDb
    cinema_houses = models.ManyToManyField(CinemaHouse)
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.movie_title} on {self.date} {self.time}"
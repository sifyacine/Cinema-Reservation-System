# cinema/models.py

from django.db import models

class Cinema(models.Model):
    id= models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email_contact = models.EmailField(max_length=254)
    rating = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=10)


class Showtime(models.Model):
    movie_title = models.CharField(max_length=255)  # Movie title from IMDb
    cinema_house = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.movie_title} at {self.cinema_house.name} on {self.date} {self.time}"


from django.db import models


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # For simplicity, store the password as plain text. In production, use hashing.
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    town_or_city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # favorite_movies = models.ManyToManyField('YourApp.Movie', blank=True)
    # favorite_cinema_houses = models.ManyToManyField('YourApp.CinemaHouse', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

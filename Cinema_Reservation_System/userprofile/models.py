from django.db import models
from authentication.models import UserProfile


class Profile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # favorite_movies = models.ManyToManyField('movie_listings.Movie', related_name='users', blank=True)
    # favorite_cinema_houses = models.ManyToManyField('cinema_houses', related_name='users', blank=True)
    # Add any additional fields you need for user profile

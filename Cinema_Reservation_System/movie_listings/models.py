from django.db import models

from authentication.models import UserProfile


class MovieSelection(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    is_interested = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    synopsis = models.TextField()
    duration = models.DurationField()
    cast = models.ManyToManyField('Actor')
    director = models.ForeignKey('Director', on_delete=models.CASCADE)
    poster = models.ImageField(upload_to='movie_posters/')
    trailer_url = models.URLField()

    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    reviews = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_movies_by_genre(cls, genre_name):
        return cls.objects.filter(genre__name=genre_name)

    @classmethod
    def get_movies_by_director(cls, director_name):
        return cls.objects.filter(director__name=director_name)

    @classmethod
    def get_top_rated_movies(cls, num_movies=5):
        return cls.objects.order_by('-rating')[:num_movies]
    

from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
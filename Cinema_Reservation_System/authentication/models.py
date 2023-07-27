from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # For simplicity, store the password as plain text. In production, use hashing.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
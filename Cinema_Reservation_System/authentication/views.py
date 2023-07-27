# authentication/views.py

from rest_framework import generics
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

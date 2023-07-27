from rest_framework.generics import CreateAPIView
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileCreateView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

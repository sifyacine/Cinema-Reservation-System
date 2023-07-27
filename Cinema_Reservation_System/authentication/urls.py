# authentication/urls.py

from django.urls import path
from .views import UserProfileCreateView

urlpatterns = [
    path('signup/', UserProfileCreateView.as_view(), name='signup'),
]

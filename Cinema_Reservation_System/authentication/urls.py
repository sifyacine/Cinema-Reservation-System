from django.urls import path
from .views import UserProfileCreateView, SignInView

urlpatterns = [
    path('signup/', UserProfileCreateView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='sign_in'),
]

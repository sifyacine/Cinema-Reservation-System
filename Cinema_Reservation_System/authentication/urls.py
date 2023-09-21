from django.urls import path
from .views import sign_in_view, sign_up_view, forgot_password, reset_password, user_profile
urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('signin/', sign_in_view, name='signin'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:email>/', reset_password, name='reset_password'),
    path('profile/',user_profile, name='user_profile'),
]

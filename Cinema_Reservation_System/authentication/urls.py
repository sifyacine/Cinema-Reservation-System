from django.urls import path
from .views import sign_in_view, sign_up_view

urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('signin/', sign_in_view, name='sign_in'),
]

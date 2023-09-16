from django.urls import path
from . import views

app_name = 'cinema_houses'

urlpatterns = [
    path('cinema_houses/', views.cinema_house_list, name='cinema_house_list'),
]
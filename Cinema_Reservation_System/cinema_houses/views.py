from django.shortcuts import render
from .models import CinemaHouse

def cinema_house_list(request):
    cinema_houses = CinemaHouse.objects.all()
    context = {
        'cinema_houses': cinema_houses
    }
    return render(request, 'cinema_house_list.html', context)

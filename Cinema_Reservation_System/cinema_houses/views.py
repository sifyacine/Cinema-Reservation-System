from django.shortcuts import render
from .models import Cinema

def cinema_house_list(request):
    cinema_houses = Cinema.objects.all()
    context = {
        'cinema_houses': cinema_houses
    }
    return render(request, 'cinema_house_list.html', context)

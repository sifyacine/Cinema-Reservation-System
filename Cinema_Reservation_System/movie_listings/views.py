import requests
from django.shortcuts import render
import json

def home(request):
    search_query = request.GET.get('q', '')
    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q": search_query}

    headers = {
        "X-RapidAPI-Key": "267d1e536cmsh11fd6bf52fc5da3p122232jsn7727a8e8e897",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    raw_response = response.text

    # Print the raw response for debugging
    print(raw_response)

    try:
        movies_data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {str(e)}")
        movies_data = []

    context = {
        'movies_data': movies_data,
        'search_query': search_query,
    }

    return render(request, 'movies_home.html', context)



import requests
from django.shortcuts import render
import json

def movie_details(request, imdb_id):
    # Replace 'YOUR_RAPIDAPI_KEY' with your actual RapidAPI key
    rapidapi_key = '267d1e536cmsh11fd6bf52fc5da3p122232jsn7727a8e8e897'

    # Define the endpoint URL for fetching movie details
    url = f"https://imdb8.p.rapidapi.com/title/get-overview-details"

    # Set query parameters
    querystring = {"tconst": imdb_id}

    # Set headers with your RapidAPI key
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    # Make the GET request to the RapidAPI endpoint
    response = requests.get(url, headers=headers, params=querystring)
    raw_response = response.text

    try:
        movie_data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {str(e)}")
        movie_data = {}

    context = {'movie_data': movie_data}
    return render(request, 'imdb_movie_details.html', context)





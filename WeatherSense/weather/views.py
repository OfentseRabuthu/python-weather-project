import requests
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import RecentSearch

def get_weather_data(city):
    # Get coordinates for the city
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={settings.OPENWEATHER_API_KEY}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if not geocoding_data:
        return None

    lat, lon = geocoding_data[0]['lat'], geocoding_data[0]['lon']

    # Get weather data
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    return weather_data

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        weather_data = get_weather_data(city)

        if weather_data:
            # Save recent search
            RecentSearch.objects.create(city_name=city)

            context = {
                'city': city,
                'current': weather_data['current'],
                'daily': weather_data['daily'][:7],
            }
            return render(request, 'weather/index.html', context)
        else:
            error_message = "City not found. Please try again."
            return render(request, 'weather/index.html', {'error': error_message})

    recent_searches = RecentSearch.objects.all()[:5]
    return render(request, 'weather/index.html', {'recent_searches': recent_searches})

def autocomplete(request):
    if 'term' in request.GET:
        qs = RecentSearch.objects.filter(city_name__icontains=request.GET.get('term'))
        cities = list(set([city.city_name for city in qs]))
        return JsonResponse(cities, safe=False)
    return JsonResponse([], safe=False)
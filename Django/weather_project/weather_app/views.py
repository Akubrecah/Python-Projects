from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .utils import get_weather_data
from .models import SearchedCity
from django.conf import settings

def weather_dashboard(request):
    city = request.GET.get('city', 'London')  # Default city
    weather_data = None
    error = None
    history = SearchedCity.objects.order_by('-searched_at')[:5]

    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            if weather_data['cod'] != 200:
                error = weather_data['message']
            else:
                # Save searched city
                SearchedCity.objects.get_or_create(name=city)
        else:
            error = "API Error"

    context = {
        'weather': weather_data,
        'error': error,
        'history': history,
        'city': city
    }
    return render(request, 'dashboard.html', context)
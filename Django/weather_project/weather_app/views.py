from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .utils import get_weather_data
from .models import SearchedCity
from django.conf import settings
import requests
from datetime import datetime

def weather_dashboard(request):
    # Default to London if no city parameter
    city = request.GET.get('city', 'London').strip()
    weather_data = None
    error = None
    history = SearchedCity.objects.order_by('-searched_at')[:5]

    if city:
        weather_data = get_weather_data(city)
        
        if weather_data:
            # Handle API error responses
            if weather_data.get('cod') != 200:  # Use .get() for safer access
                error = weather_data.get('message', 'Unknown API error')
            else:
                try:
                    # Update existing or create new
                    obj, created = SearchedCity.objects.get_or_create(name=city)
                    if not created:
                        obj.searched_at = datetime.now()
                        obj.save()
                except Exception as e:
                    # Log error but don't break the app
                    print(f"Error saving city: {e}")
        else:
            error = "API service unavailable"

    context = {
        'weather': weather_data,
        'error': error,
        'history': history,
        'city': city
    }
    return render(request, 'dashboard.html', context)
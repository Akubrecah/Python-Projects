# weather_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Main weather page
    path('forecast/', views.forecast, name='forecast'),  # Example additional route
]
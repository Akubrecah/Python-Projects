"""
URL configuration for weather_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include  # Added include import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather_app.urls')),  # Include weather app URLs
]
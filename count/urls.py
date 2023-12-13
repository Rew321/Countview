
from django.contrib import admin
from django.urls import path
from count import views 
from count.views import indexView,EventDetailView,GeocodingView,DistanceView
from django.views import generic

urlpatterns = [
    path('', indexView.as_view(), name="home"),
    path('detail/<int:pk>/', EventDetailView.as_view(), name="detail"),
    path("geocoding<int:pk>/", GeocodingView.as_view(), name="geocoding"),
    path("distance", DistanceView.as_view(), name="my_distance_view"),
    
]
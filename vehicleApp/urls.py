# vehicleApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create_vehicle/', views.create_vehicle, name='create_vehicle'),
    path('vehicle_detail/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('update_vehicle/<int:pk>/', views.update_vehicle, name='update_vehicle'),
    path('delete_vehicle/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('list_vehicles/', views.list_vehicles, name='list_vehicles'),
    path('search_vehicle_by_type/', views.search_vehicle_by_type, name='search_vehicle_by_type'),
    path('total_vehicles/', views.total_vehicles, name='total_vehicles'),
    path('vehicles_by_total_weight/', views.vehicles_by_total_weight, name='vehicles_by_total_weight'),
    path('vehicles_by_price_per_km/', views.vehicles_by_price_per_km, name='vehicles_by_price_per_km'),
    path('vehicle_stats/', views.vehicle_stats, name='vehicle_stats'),
    path('download_vehicles/', views.download_vehicles, name='download_vehicles'),
]


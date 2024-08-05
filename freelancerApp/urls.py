from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_freelancer, name='create_freelancer'),
    path('freelancers/', views.get_all_freelancers, name='get_all_freelancers'),
    path('detail/<int:pk>/', views.freelancer_detail, name='freelancer_detail'),
    path('update/<int:pk>/', views.update_freelancer, name='update_freelancer'),
    path('delete/<int:pk>/', views.delete_freelancer, name='delete_freelancer'),
    path('search_by_name/<str:name>/', views.find_freelancer_by_name, name='find_freelancer_by_name'),
    path('by_address/<str:address>/', views.get_freelancers_by_address, name='get_freelancers_by_address'),
    path('by_vehicle_type/<str:type>/', views.get_freelancers_by_vehicle_type, name='get_freelancers_by_vehicle_type'),
    path('total/', views.get_total_freelancers, name='get_total_freelancers'),
    path('growth/', views.freelancer_growth, name='freelancer_growth'),
    path('download/excel/', views.download_freelancers_excel, name='download_freelancers_excel'),
    path('download/csv/', views.download_freelancers_csv, name='download_freelancers_csv'),
    path('approve/<int:pk>/', views.approve_freelancer, name='approve_freelancer'),  # New URL for approving a freelancer
]

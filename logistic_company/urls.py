# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.display_all_companies, name='display_all_companies'),
    path('create/', views.create_company, name='create_company'),
    path('<int:pk>/', views.get_company_by_id, name='get_company_by_id'),
    path('name/<str:name>/', views.get_company_by_name, name='get_company_by_name'),
    path('location/<str:location>/', views.get_companies_by_location, name='get_companies_by_location'),
    path('update<int:pk>/', views.update_company, name='update_company'),
    path('delete<int:pk>/', views.delete_company, name='delete_company'),
    path('status/<str:status>/', views.get_companies_by_status, name='get_companies_by_status'),
]


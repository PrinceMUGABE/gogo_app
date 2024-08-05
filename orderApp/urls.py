from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('orders/', views.display_all_orders, name='display_all_orders'),
    path('get_by_id/<int:pk>/', views.get_order_by_id, name='get_order_by_id'),
    path('name/<str:name>/', views.get_order_by_name, name='get_order_by_name'),
    path('type/<int:vehicle_type_id>/', views.get_orders_by_vehicle_type, name='get_orders_by_vehicle_type'),
    path('delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('update/<int:pk>/', views.update_order, name='update_order'),
    path('download/pdf/', views.download_orders_pdf, name='download_orders_pdf'),
    path('download/excel/', views.download_orders_excel, name='download_orders_excel'),
    path('download/csv/', views.download_orders_csv, name='download_orders_csv'),
]

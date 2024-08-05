# trackingApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_tracking, name='create_tracking'),
    path('<int:id>/', views.get_tracking_by_id, name='get_tracking_by_id'),
    path('list/', views.list_all_tracking, name='list_all_tracking'),
    path('list/longitude/<str:longitude>/', views.list_tracking_by_longitude, name='list_tracking_by_longitude'),
    path('list/latitude/<str:latitude>/', views.list_tracking_by_latitude, name='list_tracking_by_latitude'),
    path('car/<int:car_id>/', views.get_tracking_by_car, name='get_tracking_by_car'),
    path('update/<int:id>/', views.update_tracking_by_id, name='update_tracking_by_id'),
    path('delete/<int:id>/', views.delete_tracking_by_id, name='delete_tracking_by_id'),
]

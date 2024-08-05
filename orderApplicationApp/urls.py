# orderApplicationApp/urls.py
from django.urls import path
from .views import (
    CreateOrderApplication, OrderApplicationDetail, OrderApplicationByOrder,
    OrderApplicationByFreelancer, UpdateOrderApplication, DeleteOrderApplication,
    ListOrderApplications, OrderApplicationsByStatus
)

urlpatterns = [
    path('create/', CreateOrderApplication.as_view(), name='create_order_application'),
    path('<int:id>/', OrderApplicationDetail.as_view(), name='order_application_detail'),
    path('order/<int:order_id>/', OrderApplicationByOrder.as_view(), name='order_application_by_order'),
    path('freelancer/<int:freelancer_id>/', OrderApplicationByFreelancer.as_view(), name='order_application_by_freelancer'),
    path('update/<int:id>/', UpdateOrderApplication.as_view(), name='update_order_application'),
    path('delete/<int:id>/', DeleteOrderApplication.as_view(), name='delete_order_application'),
    path('all/', ListOrderApplications.as_view(), name='list_order_applications'),
    path('status/<str:status>/', OrderApplicationsByStatus.as_view(), name='order_applications_by_status'),
]

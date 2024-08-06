from django.urls import path
from .views import (
    create_payment,
    display_all_payments,
    get_payment_by_id,
    get_payment_by_order,
    get_payments_by_status,
    get_payments_by_provider,
    get_payments_by_kind,
    update_payment,
    delete_payment,
    get_orders_by_user
)

urlpatterns = [
    path('payments/', display_all_payments, name='display_all_payments'),
    path('payments/create/', create_payment, name='create_payment'),
    path('payments/<int:pk>/', get_payment_by_id, name='get_payment_by_id'),
    path('payments/order/<int:order_id>/', get_payment_by_order, name='get_payment_by_order'),
    path('payments/status/<str:status>/', get_payments_by_status, name='get_payments_by_status'),
    path('payments/provider/<str:provider>/', get_payments_by_provider, name='get_payments_by_provider'),
    path('payments/kind/<str:kind>/', get_payments_by_kind, name='get_payments_by_kind'),
    path('payments/update/<int:pk>/', update_payment, name='update_payment'),
    path('payments/delete/<int:pk>/', delete_payment, name='delete_payment'),
    path('orders/user/<int:user_id>/', get_orders_by_user, name='get_orders_by_user'),
]

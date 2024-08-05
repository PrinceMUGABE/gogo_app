from django.urls import path
from .views import (
    CreateDiscountOrder, DiscountOrderDetail, UpdateDiscountOrder,
    DeleteDiscountOrder, ListDiscountOrders
)

urlpatterns = [
    path('create/', CreateDiscountOrder.as_view(), name='create_discount_order'),
    path('<int:id>/', DiscountOrderDetail.as_view(), name='discount_order_detail'),
    path('update/<int:id>/', UpdateDiscountOrder.as_view(), name='update_discount_order'),
    path('delete/<int:id>/', DeleteDiscountOrder.as_view(), name='delete_discount_order'),
    path('all/', ListDiscountOrders.as_view(), name='list_discount_orders'),
]

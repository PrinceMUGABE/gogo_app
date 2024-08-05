from rest_framework import generics, permissions
from .models import DiscountOrder
from .serializers import DiscountOrderSerializer

class CreateDiscountOrder(generics.CreateAPIView):
    queryset = DiscountOrder.objects.all()
    serializer_class = DiscountOrderSerializer
    permission_classes = [permissions.IsAdminUser, permissions.DjangoModelPermissions]

class DiscountOrderDetail(generics.RetrieveAPIView):
    queryset = DiscountOrder.objects.all()
    serializer_class = DiscountOrderSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser, permissions.DjangoModelPermissions]

class UpdateDiscountOrder(generics.UpdateAPIView):
    queryset = DiscountOrder.objects.all()
    serializer_class = DiscountOrderSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser, permissions.DjangoModelPermissions]

class DeleteDiscountOrder(generics.DestroyAPIView):
    queryset = DiscountOrder.objects.all()
    serializer_class = DiscountOrderSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAdminUser, permissions.DjangoModelPermissions]

class ListDiscountOrders(generics.ListAPIView):
    queryset = DiscountOrder.objects.all()
    serializer_class = DiscountOrderSerializer
    permission_classes = [permissions.IsAdminUser, permissions.DjangoModelPermissions]

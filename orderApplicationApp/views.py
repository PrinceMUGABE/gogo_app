# orderApplicationApp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import OrderApplication
from .serializers import OrderApplicationSerializer
from orderApp.models import Order


class CreateOrderApplication(generics.CreateAPIView):
    queryset = OrderApplication.objects.all()
    serializer_class = OrderApplicationSerializer
    permission_classes = [IsAuthenticated]

class OrderApplicationDetail(generics.RetrieveAPIView):
    queryset = OrderApplication.objects.all()
    serializer_class = OrderApplicationSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    

class OrderApplicationByOrder(generics.ListAPIView):
    serializer_class = OrderApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderApplication.objects.filter(order_id=order_id)
        
    
    

class OrderApplicationByFreelancer(generics.ListAPIView):
    serializer_class = OrderApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        freelancer_id = self.kwargs['freelancer_id']
        return OrderApplication.objects.filter(freelancer_id=freelancer_id)
    

class UpdateOrderApplication(generics.UpdateAPIView):
    queryset = OrderApplication.objects.all()
    serializer_class = OrderApplicationSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'delivered' or instance.status == 'failed':
            instance.order.status = True  # Set order to available if the application is delivered or failed
            instance.order.save()

class DeleteOrderApplication(generics.DestroyAPIView):
    queryset = OrderApplication.objects.all()
    serializer_class = OrderApplicationSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class ListOrderApplications(generics.ListAPIView):
    queryset = OrderApplication.objects.all()
    serializer_class = OrderApplicationSerializer
    permission_classes = [IsAuthenticated]

class OrderApplicationsByStatus(generics.ListAPIView):
    serializer_class = OrderApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status = self.kwargs['status']
        return OrderApplication.objects.filter(status=status)

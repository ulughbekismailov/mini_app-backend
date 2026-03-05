from products.models import Order
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action

from products.serializers import OrderSerializer


class AdminOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['id']

    def get_queryset(self):
        return Order.objects.order_by('-created_at')

    http_method_names = ['get', 'patch', 'delete']

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        order.status = request.data['status']
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
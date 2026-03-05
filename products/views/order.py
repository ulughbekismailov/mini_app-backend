from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from products.models import Cart, Order, OrderItem
from products.serializers import OrderSerializer, OrderCreateSerializer
from products.user_authentication import TelegramAuth




class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = [TelegramAuth]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart is not Found!!!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cart.items.exists():
            return Response(
                {'error': 'Savat bo\'sh'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order = Order.objects.create(
            customer=request.user,
            phone_number=data.get('phone_number', ''),
            shipping_address=data['shipping_address'],
            notes=data.get('notes', ''),
            total_price=0,
            status=Order.PENDING
        )

        total = 0
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            total += cart_item.product.price * cart_item.quantity

        order.total_price = total
        order.save()

        cart.items.all().delete()

        response_serializer = self.get_serializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

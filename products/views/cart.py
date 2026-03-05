from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Cart, CartItem, Product
from products.serializers import CartSerializer

from products.user_authentication import TelegramAuth
from rest_framework.permissions import IsAuthenticated

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    authentication_classes = [TelegramAuth]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Savatga mahsulot qo‘shish yoki miqdorini oshirish"""
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        # MUHIM: get_or_create – mahsulot savatda bo‘lsa, yangilaydi
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not created:
            # Agar avvaldan bo‘lsa, miqdorini oshiramiz
            item.quantity += quantity
            item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        """Mahsulot miqdorini o‘zgartirish yoki o‘chirish"""
        cart = self.get_object()
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity'))

        item = CartItem.objects.get(id=item_id, cart=cart)
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Mahsulotni savatdan butunlay o‘chirish"""
        cart = self.get_object()
        item_id = request.query_params.get('item_id')
        CartItem.objects.filter(id=item_id, cart=cart).delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Savatni tozalash"""
        cart = self.get_object()
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
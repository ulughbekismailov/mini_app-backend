from rest_framework import serializers
from products.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.CharField(source='product.id', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_telegram_id = serializers.CharField(source='customer.telegram_id', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_username', 'customer_name', 'customer_telegram_id', 'confirmed_by_user',
            'phone_number', 'shipping_address', 'notes', 'status',
            'total_price', 'created_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'total_price', 'customer', 'customer_telegram_id']


class OrderCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, allow_blank=True)
    shipping_address = serializers.CharField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
from rest_framework import serializers
from products.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", 'product_id','product_name', 'product_price', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

class CartSerializer(serializers.ModelSerializer):
    # MUHIM: read_only=True bo'lishi shart!
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['items', 'total_items', 'subtotal']

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_subtotal(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())
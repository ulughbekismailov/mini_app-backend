from rest_framework import serializers

from products.models import ProductLike


class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = '__all__'

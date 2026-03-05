import os

from rest_framework import serializers
from products.models import ProductImage

DOMEN = os.environ.get("DOMEN")


class ProductImageReadSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main", "order"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return f"{DOMEN}{obj.image.url}"


class ProductImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False
    )
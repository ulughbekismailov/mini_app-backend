from rest_framework import generics, status
from rest_framework.response import Response

from products.models import Product, ProductImage
from products.serializers import (
    ProductImageReadSerializer,
    ProductImageUploadSerializer
)
from products.services.product_image import add_images, delete_image


class ProductImageListCreateAPIView(generics.GenericAPIView):
    serializer_class = ProductImageUploadSerializer

    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        images = product.images.all()
        serializer = ProductImageReadSerializer(images, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.validated_data.get("images")
        created_images = add_images(product, images)
        read_serializer = ProductImageReadSerializer(created_images, many=True, context={"request": request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class ProductImageDeleteAPIView(generics.DestroyAPIView):
    queryset = ProductImage.objects.all()

    def delete(self, request, pk):
        image = self.get_object()
        delete_image(image)
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework import viewsets, serializers
from products.models import ProductLike
from products.serializers import ProductLikeSerializer


class ProductLikeViewSet(viewsets.ModelViewSet):
    queryset = ProductLike.objects.all()
    serializer_class = ProductLikeSerializer

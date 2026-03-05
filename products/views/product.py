from rest_framework import viewsets, filters
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from products.user_authentication import TelegramAuth

from products.models import Product
from products.serializers import ProductSerializer


class ProductCursorPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50
    ordering = '-created_at'
    cursor_query_param = 'cursor'


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = [TelegramAuth]
    permission_classes = [IsAuthenticated]

    pagination_class = ProductCursorPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).prefetch_related(
            'images'
        ).select_related(
            'category'
        ).order_by('-created_at')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
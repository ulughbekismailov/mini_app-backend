from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from products.serializers import ProductSerializer


class ProductAdminViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    # Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'category': ['exact'],
        'is_active': ['exact'],
    }

    search_fields = ['name', 'description']

    ordering_fields = ['price', 'sold_count', 'name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images').all()

        discount_active = self.request.query_params.get('discount_active')
        if discount_active is not None:
            if discount_active == 'true':
                queryset = queryset.filter(
                    discount_percent__isnull=False,
                )

        return queryset

    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()

        return Response(
            {
                "id": product.id,
                "is_active": product.is_active
            },
            status=status.HTTP_200_OK
        )
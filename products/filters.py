from django_filters import rest_framework as rest_filters
from .models import Product


class ProductFilter(rest_filters.FilterSet):
    min_price = rest_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = rest_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

from rest_framework import viewsets, filters

from products.models import Category, TelegramUser
from products.serializers import CategorySerializer, TelegramUserSerializer

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    filter_backends = [filters.SearchFilter]

    search_fields = ['name']

class UserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    filter_backends = [filters.SearchFilter]

    search_fields = ['first_name', 'last_name', 'username']

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from products.models import ProductLike
from products.serializers import ProductLikeSerializer

from products.user_authentication import TelegramAuth
from rest_framework.permissions import IsAuthenticated

class ProductLikeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductLikeSerializer
    authentication_classes = [TelegramAuth]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductLike.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response(
                {'error': 'product_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        liked_obj = self.get_queryset().filter(product_id=product_id).first()

        if liked_obj:
            liked_obj.delete()
            return Response({'liked': False})
        else:
            like = ProductLike.objects.create(
                user=request.user,
                product_id=product_id
            )
            serializer = self.get_serializer(like)
            return Response({'liked': True, 'data': serializer.data})

    @action(detail=False, methods=['get'])
    def my_likes(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
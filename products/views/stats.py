from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Order


class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        month_ago = now - timedelta(days=30)

        total_orders = Order.objects.count()
        pending = Order.objects.filter(status='Pending').count()
        delivered = Order.objects.filter(status='Delivered').count()

        revenue = Order.objects.filter(
            status='Delivered'
        ).aggregate(total=Sum('total_price'))['total'] or 0

        return Response({
            'total_orders': total_orders,
            'pending_orders': pending,
            'delivered_orders': delivered,
            'total_revenue': revenue,
        })


class TopProductsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        top_products = Product.objects.filter(
            sold_count__gt=0
        ).order_by('-sold_count')[:10]

        data = [{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'sold_count': p.sold_count,
        } for p in top_products]

        return Response({'results': data})


class MonthlyOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Oxirgi 6 oylik statistika
        now = timezone.now()
        months = []
        data = []

        for i in range(5, -1, -1):
            month = now - timedelta(days=30 * i)
            month_name = month.strftime('%b')  # Jan, Feb, ...
            months.append(month_name)

            # Shu oydagi buyurtmalar soni
            month_start = month.replace(day=1, hour=0, minute=0, second=0)
            if i == 0:
                month_end = now
            else:
                month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

            count = Order.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).count()
            data.append(count)

        return Response({
            'labels': months,
            'data': data
        })
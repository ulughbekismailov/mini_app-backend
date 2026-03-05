from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet, ProductAdminViewSet, CategoryViewSet, UserViewSet, ProductImageListCreateAPIView, ProductImageDeleteAPIView
from products.views import CartViewSet, OrderViewSet, ProductLikeViewSet, AdminOrderViewSet, DashboardStatsView, TopProductsView, MonthlyOrdersView

router = DefaultRouter()
router.register(r'products', ProductViewSet,  basename='product')
router.register(r'categories', CategoryViewSet)
router.register('cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'likes', ProductLikeViewSet, basename='like')
router.register(r'telegram-users', UserViewSet, basename='telegram-users')

admin_router = DefaultRouter()
admin_router.register(r'products', ProductAdminViewSet, basename='admin-product')
admin_router.register(r'orders', AdminOrderViewSet, basename='admin-order')
admin_router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', include(admin_router.urls)),

    path('admin/products/<int:product_id>/images/', ProductImageListCreateAPIView.as_view(),
         name='product-image-list-create'),

    path('admin/images/<int:pk>/delete/', ProductImageDeleteAPIView.as_view(),
         name='product-image-delete'),

    path('admin/dashboard/stats/', DashboardStatsView.as_view()),
    path('admin/dashboard/top-products/', TopProductsView.as_view()),
    path('admin/dashboard/monthly-orders/', MonthlyOrdersView.as_view()),
]


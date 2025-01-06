from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . views import ProductViewSet, CustomerViewSet, CategoryViewset, OrderViewset, CartViewSet, CartItemViewSet, ReviewViewSet

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products'),
router.register(r'customers', CustomerViewSet, basename='customers'),
router.register(r'categories', CategoryViewset, basename='categories'),
router.register(r'orders', OrderViewset),
router.register(r'carts', CartViewSet),

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet,
                         basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart_items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(carts_router.urls)),
]

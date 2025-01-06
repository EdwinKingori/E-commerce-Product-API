from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import ProductViewSet, CustomerViewSet, CategoryViewset, OrderViewset, CartViewSet

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products'),
router.register(r'customers', CustomerViewSet, basename='customers'),
router.register(r'categories', CategoryViewset, basename='categories'),
router.register(r'orders', OrderViewset),
router.register(r'carts', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

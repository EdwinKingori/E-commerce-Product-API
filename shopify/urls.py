from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import ProductViewSet, CustomerViewSet, CategoryViewset

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products'),
router.register(r'customers', CustomerViewSet, basename='customers'),
router.register(r'categories', CategoryViewset, basename='categories'),


urlpatterns = [
    path('', include(router.urls)),
]

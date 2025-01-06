from django.db.models.aggregates import Count
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer, OrderSerializer, CartSerializer, CartItemSerializer
from .models import Product, Customer, Category, Order, OrderItem, Cart, CartItem
from .pagination import DefaultPagination
# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('products')
    ).all()
    serializer_class = CategorySerializer

    # overriding the modelviewset's destroy method
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(category_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Category cannot be deleted beacuse it includes one or more products!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    pagination_class = DefaultPagination
    ordering_fields = ['unitprice', 'last_update']

    def get_queryset(self):
        return Product.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = DefaultPagination


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    # prefetch_related reduces the query used to get the needed items
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    pass

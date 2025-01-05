from django.db.models.aggregates import Count
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer, OrderSerializer
from .models import Product, Customer, Category, Order, OrderItem
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
    ordering_fields = ['unitprice', 'last_update']

    def get_queryset(self):
        return Product.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

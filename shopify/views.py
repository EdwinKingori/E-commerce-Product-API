from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ProductSerializer, CategorySerializer, CustomerSerializer
from .models import Product, Customer
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

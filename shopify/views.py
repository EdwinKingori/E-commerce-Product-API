from django.db.models.aggregates import Count
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import NotAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .serializers import (ProductSerializer,
                          CategorySerializer,
                          CustomerSerializer,
                          ReviewSerializer,
                          OrderSerializer,
                          CartSerializer,
                          CartItemSerializer,
                          AddItemSerializer,
                          UpdateCartItemSerializer
                          )
from .permissions import IsAdminOrReadOnly
from .models import Product, Customer, Category, Order, OrderItem, Cart, CartItem, Review
from .pagination import DefaultPagination
# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(
        products_count=Count('products')
    ).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'description']
    pagination_class = DefaultPagination
    ordering_fields = ['unitprice', 'last_update']

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({"error": "Selected product cannot be deleted beacuse it is associated with an order item. "}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    # prefetch_related reduces the query used to get the needed items
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    # utilizing htttp methods
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    # configuring getting a users/customer's profile
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated(
                "You must be logged in to access this endpoint.")

        customer, created = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)

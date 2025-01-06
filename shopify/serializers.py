from rest_framework import serializers
from .models import Product, Category, Customer, Order, OrderItem, Review, Cart, CartItem
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'slug', 'unitprice', 'price_with_tax',
                  'stock_quantity', 'image_url', 'category']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unitprice * Decimal(1.1)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'birthdate']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'payment_status', 'placed_at']

# using this simpeproductserializer when returning basic product information is needed


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unitprice']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unitprice

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # cannot send it to server
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_price']

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unitprice for item in cart.items.all()])

    # alternative for the above method
    # def get_total_price(self, cart: Cart):
    #     total_price = 0
    #     for item in cart.items.all():
    #         total_price += item.quantity * item.product.unitprice
    #     return total_price


class AddItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_data(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "No product with the given id was found!"
            )
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.context['product_id']
        quantity = self.context['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)  # replaced product_id=product_id, quantity_id=quantity_id with the **self.validated_data

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelField):
    class Meta:
        model = CartItem
        fields = ['quantity']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'name', 'description']

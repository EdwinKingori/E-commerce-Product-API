from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Product, Category, Customer, Order, OrderItem, Review, Cart, CartItem


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


# using this SimpleProductSerializer when returning basic product information is desired, mostly when returning to clients.
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unitprice']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'first_name',
                  'last_name', 'phone', 'birthdate']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'payment_status', 'placed_at', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


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

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unitprice for item in cart.items.all()])

    # alternative for the above method
    # def get_total_price(self, cart: Cart):
    #     total_price = 0
    #     for item in cart.items.all():
    #         total_price += item.quantity * item.product.unitprice
    #     return total_price

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'name', 'description']

# Adding custm serializers


class AddItemSerializer(serializers.ModelSerializer):
    # explicitly defining the product_id field
    product_id = serializers.IntegerField()

    # validating the value of product_id
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "No product with the given id was found!"
            )
        return value

    # overwriting the modelserializer's save method.
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

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


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given id exists!')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty!')
        return cart_id

    def save(self, **kwargs):
        # using django transactions to ensure the database remains in consistent state even if something goes wrong
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            customer, create = Customer.objects.get_or_create(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            # creating order items
            cart_items = CartItem.objects. select_related('product').filter(
                cart_id=cart_id)
            # using listcomprehension to convert cart_items to order items
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unitprice,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            # enabling deleting the cart
            Cart.objects.filter(pk=cart_id).delete()

            return order

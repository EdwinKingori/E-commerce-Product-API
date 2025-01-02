from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Category, Product, Customer, Order, OrderItem, Cart, CartItem
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, category):
        # syntax for reverse (custom url): app_model_targetmodel_changelist
        url = (reverse('admin:shopify_product_changelist')
               + '?'
               + urlencode({
                   'category__id': str(category.id)
               }))
        return format_html('<a href="{}">{}</a>', url, category.products_count)

# since the collection object does not have a fied by the name products_count
# we need to overwrite the queryset on this page and annotate the collections with the numberof their products.
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


# creating a custom filter that allows admin to check products with low stock or inventory.
class StockFilter(admin.SimpleListFilter):
    title = 'stock_count'
    parameter_name = 'stock_count'

    def lookups(self, request, model_admin):
        return [
            ('<10', "Low")
        ]

    def get_queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(stock_count__lt=10)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'unitprice', 'stock_status', 'category_title']
    list_editable = ['unitprice']
    list_per_page = 10
    # loading a related object (category) in the list page using the 'category_title' function
    list_select_related = ['category']
    list_filter = ['category', 'last_update', StockFilter]

    def category_title(self, product):
        return product.category.title

    @admin.display(ordering='stock_quantity')
    def stock_status(self, value):
        if Product.stock_quantity < 10:
            return 'Low'
        return 'OK'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'orders_count']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:shopify_order_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)

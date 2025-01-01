from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, Cart, CartItem
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'unitprice', 'stock_status', 'category_title']
    list_editable = ['unitprice']
    list_per_page = 10
    # loading a related object (category) in the list page using the 'category_title' function
    list_select_related = ['category']

    def category_title(self, product):
        return product.category.title

    @admin.display(ordering='stock_quantity')
    def stock_status(self, value):
        if Product.stock_quantity < 10:
            return 'Low'
        return 'OK'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['user__first_name', 'user__last_name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)

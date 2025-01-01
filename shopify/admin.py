from django.contrib import admin
from .models import Category, Product, Customer, Order, OrderItem, Cart, CartItem
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'unitprice', 'stock_status']
    list_editable = ['unitprice']
    list_per_page = 10

    @admin.display(ordering='stock_quantity')
    def stock_status(self, value):
        if Product.stock_quantity < 10:
            return 'Low'
        return 'OK'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['user__first_name', 'user__last_name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)

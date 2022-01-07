from django.contrib import admin
from .models import Payment, Order, OrderedProduct
# Register your models here.


class OrderedProductAdmin(admin.TabularInline):
    model = OrderedProduct
    extra = 0
    read_only_fields = ['payment', 'user', 'product', 'productVariant', 'quantity', 'productPrice', 'ordered', 'createdAt', 'updatedAt']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderNumber', 'fullName', 'phone_number', 'email', 'paymentMethod', 'orderStatus', 'isOrdered', 'createdAt']
    list_filter = ['paymentMethod', 'orderStatus', 'isOrdered', 'createdAt']
    search_fields = ['paymentMethod', 'orderNumber', 'fullName', 'email']
    list_per_page = 30
    inlines = [OrderedProductAdmin]
    
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedProduct)

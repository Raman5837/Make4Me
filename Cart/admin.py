from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ['cartId', 'date_added']
    list_filter = ['date_added']
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'isActive', 'cart']
    list_filter = ['product', 'isActive']
    list_display_links = ['product']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
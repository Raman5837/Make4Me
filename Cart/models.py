from django.db import models
from StoreRoom.models import Product, ProductVariants, ProductCustomization
from Accounts.models import Account
# Create your models here.


class Cart(models.Model):
    cartId = models.CharField(max_length = 250, blank = True, verbose_name = 'Cart Id')
    date_added = models.DateTimeField(auto_now_add = True, verbose_name = 'Date Added')
    
    def __str__(self):
        return self.cartId 
    
class CartItem(models.Model):
    
    user = models.ForeignKey(Account, on_delete = models.CASCADE, null = True)
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null = True)
    productCustomization = models.ForeignKey(ProductCustomization, on_delete = models.CASCADE, null = True)
    
    productVariant = models.ManyToManyField(ProductVariants, blank = True, verbose_name = 'Product Variant')
    quantity = models.PositiveIntegerField(verbose_name = 'Quantity')
    isActive = models.BooleanField(default = True, verbose_name = 'Is Active')
    
    class meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    
    def __str__(self):
        return f'{self.product} | Quantity =  {self.quantity}'
    
    def subTotal(self):
        return self.product.discountedPrice * self.quantity
    
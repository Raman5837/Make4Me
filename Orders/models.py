from django.db import models
from Accounts.models import Account
from StoreRoom.models import Product, ProductVariants
# Create your models here.


class Payment(models.Model):
    
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
        ('Paytm', 'Paytm'),
        ('RazorPay', 'RazorPay'),
        )
    
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    paymentId = models.CharField(max_length = 150, verbose_name = 'Payment ID')
    paymentMethod = models.CharField(max_length = 150, choices = PAYMENT_METHOD, verbose_name = 'Payment Method')
    amountPaid = models.FloatField(verbose_name = 'Amount Paid')
    paymentStatus = models.CharField(max_length = 150, verbose_name = 'Payment Status')
    createdAt = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.user} {self.paymentId}'
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        
class Order(models.Model):
    
    ORDER_STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    
    user = models.ForeignKey(Account, on_delete = models.SET_NULL, null = True)
    payment = models.ForeignKey(Payment, on_delete = models.SET_NULL, null = True, blank = True)
    orderNumber = models.CharField(max_length = 20, verbose_name = 'Order Number')
    
    paymentMethod = models.CharField(max_length = 150,  verbose_name = 'Payment Method', blank = True)
    first_name = models.CharField(max_length = 50, verbose_name = 'First Name')
    last_name = models.CharField(max_length = 50, verbose_name = 'Last Name')
    phone_number = models.CharField(max_length = 15, verbose_name = 'Phone Number')
    email = models.EmailField(max_length = 50, verbose_name = 'Email')
    address_line_1 = models.CharField(max_length = 100, verbose_name = 'Address Line 1')
    address_line_2 = models.CharField(max_length = 100, verbose_name = 'Address Line 2', blank = True)
    country = models.CharField(max_length = 50, verbose_name = 'Country')
    state = models.CharField(max_length = 50, verbose_name = 'State')
    city = models.CharField(max_length = 50, verbose_name = 'City')
    pincode = models.CharField(max_length = 10, verbose_name = 'Pincode')
    order_note = models.TextField(max_length = 250, blank = True, verbose_name = 'Order Note')
    imageForCustomization1 = models.ImageField(upload_to='Images/CustomizationImages/',verbose_name='Image For Customization 1', blank = True, null = True)
    imageForCustomization2 = models.ImageField(upload_to='Images/CustomizationImages/',verbose_name='Image For Customization 2', blank = True, null = True)
    
    orderTotal = models.FloatField(verbose_name = 'Order Total')
    tax = models.FloatField(verbose_name = 'Tax')
    orderStatus = models.CharField(max_length = 10, choices = ORDER_STATUS, default = 'New', verbose_name = 'Order Status')
    ip = models.CharField(max_length = 20, blank = True, verbose_name = 'IP Address')
    isOrdered = models.BooleanField(default = False, verbose_name = 'Is Ordered')
    createdAt = models.DateTimeField(auto_now_add = True, verbose_name = 'Created At')
    updatedAt = models.DateTimeField(auto_now = True, verbose_name = 'Updated At')
    
    
    def fullName(self):
        return f'{self.first_name} {self.last_name}'
    
    def fullAddress(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def completeAddress(self):
        return f'{self.address_line_1} {self.address_line_2}, {self.city} - {self.pincode}, {self.state}, {self.country}'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        
class OrderedProduct(models.Model):
    
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'order')
    payment = models.ForeignKey(Payment, on_delete = models.SET_NULL, blank = True, null = True)
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    productVariant = models.ManyToManyField(ProductVariants, blank = True, verbose_name = 'Product Variant')

    quantity = models.PositiveIntegerField(verbose_name = 'Quantity')
    productPrice = models.FloatField(verbose_name = 'Product Price')
    ordered = models.BooleanField(default = False, verbose_name = 'Ordered')
    createdAt = models.DateTimeField(auto_now_add = True, verbose_name = 'Created At')
    updatedAt = models.DateTimeField(auto_now = True, verbose_name = 'Updated At')
    
    
    def __str__(self):
        return f'{self.product.productName}'    
    
    def QuantityXPrice(self):
        return self.quantity * self.productPrice
    
    def shippingCharge(self):
        return min(100,self.product.shippingCharge)
    
    
    class Meta:
        verbose_name = 'Ordered Product'
        verbose_name_plural = 'Ordered Products'
from django.shortcuts import render
from .models import Cart, CartItem
from .views import _cartId
from django.core.exceptions import ObjectDoesNotExist


def Counter(request, Total = 0, quantity = 0):
    
    cartCount = 0
    
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cartId = _cartId(request))
            
            if request.user.is_authenticated:
                cartItems = CartItem.objects.all().filter(user = request.user)
            else:
                cartItems = CartItem.objects.all().filter(cart = cart[:1])
            
            for cartItem in cartItems:
                cartCount += cartItem.quantity
        except Cart.DoesNotExist:
            cartCount = 0
            
        try:
            cart = Cart.objects.get(cartId = _cartId(request))
            cartItems = CartItem.objects.filter(cart = cart, isActive = True)
            
            for cartItem in cartItems:
                Total += (cartItem.product.discountedPrice * cartItem.quantity)

                quantity += (cartItem.quantity)


        except ObjectDoesNotExist:
            pass 
            
    return dict(cartCount=cartCount, cartItems = cartItems, Total = Total, quantity = quantity)

       
# def CartForNavbar(request, Total = 0, quantity = 0, cartItems = None):
    
#     try:
#         cart = Cart.objects.get(cartId = _cartId(request))
#         cartItems = CartItem.objects.filter(cart = cart, isActive = True)
#         taxDict = []
#         shippingChargeDict = []
#         for cartItem in cartItems:
#             Total += (cartItem.product.discountedPrice * cartItem.quantity)

#             quantity += (cartItem.quantity)

#             taxDict.append(cartItem.product.tax)

#             shippingChargeDict.append((cartItem.product.shippingCharge))

#         # tax = (sum(taxDict)*Total)/100
#         shippingCharge = sum(shippingChargeDict)
#         shippingCharge = min(shippingCharge, 100)

#         grandTotal = Total + shippingCharge

#     except ObjectDoesNotExist:
#         pass 

#     context = {'Total': Total, 'quantity': quantity, 'cartItems': cartItems, 'grandTotal': grandTotal, 'shippingCharge': shippingCharge}


#     return render(request, 'store/cart.html', context)
            
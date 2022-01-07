from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from StoreRoom.models import Product, ProductVariants, ProductCustomization
from .forms import ProductCustomization_Form


from .models import Cart, CartItem
# Create your views here.

def _cartId(request): # Getting Session Key From The Browser Which Will be used as cartId
    cart = request.session.session_key
    if not cart:
          cart = request.session.create()
    return cart


def AddToCart(request, productId):  # sourcery no-metrics
    
    current_user = request.user

    product = Product.objects.get(id=productId) #get the product

    product_variation = []
    if current_user.is_authenticated:
        
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                print(key, value)
                try:
                    variation = ProductVariants.objects.get(product = product, variationCategory__iexact=key, variationValue__iexact=value)
                    product_variation.append(variation)
                    print('product_variation = ', product_variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product = product, user = current_user).exists()
        if is_cart_item_exists:

            cart_item = CartItem.objects.filter(product = product, user = current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.productVariant.all()

                existing_variation_List = list(existing_variation)
                ex_var_list.append(existing_variation_List)
                id.append(item.id)


            if product_variation in ex_var_list:
                
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
            else:

                item = CartItem.objects.create(product=product, quantity=1, user = current_user)
                if product_variation:
                    item.productVariant.clear()
                    item.productVariant.add(*product_variation)
            item.save()

        else:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user
                )
            if product_variation:
                cart_item.productVariant.clear()
                cart_item.productVariant.add(*product_variation)
                cart_item.save()
    else:
        
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = ProductVariants.objects.get(product = product, variationCategory__iexact=key, variationValue__iexact=value)
                    product_variation.append(variation)
                    print('product_variation = ', product_variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cartId = _cartId(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cartId = _cartId(request))
            cart.save()

        # yha tak done


        is_cart_item_exists = CartItem.objects.filter(product=product, cart = cart).exists()
        if is_cart_item_exists:

            cart_item = CartItem.objects.filter(product=product, cart = cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.productVariant.all()
                print('existing_variation = ', existing_variation)
                existing_variation_List = list(existing_variation)
                ex_var_list.append(existing_variation_List)
                id.append(item.id)
            print('Type of existing_variation_List = ',type(existing_variation_List))

            if product_variation in ex_var_list:
                
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
            else:

                item = CartItem.objects.create(product=product, quantity=1, cart = cart)
                if product_variation:
                    item.productVariant.clear()
                    item.productVariant.add(*product_variation)
            item.save()

        else:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
                )
            if product_variation:
                cart_item.productVariant.clear()
                cart_item.productVariant.add(*product_variation)
                cart_item.save()

    return redirect('cart')
    




def DecreaseQuantity(request, productId, cartItemId):
    
    
    product = get_object_or_404(Product, id = productId)
    try:
        
        if request.user.is_authenticated:
            cartItem = CartItem.objects.get(product = product, user = request.user, id  = cartItemId)
        else:
            cart = Cart.objects.get(cartId = _cartId(request))
            cartItem = CartItem.objects.get(product = product, cart = cart, id  = cartItemId)
        
        if cartItem.quantity > 1:
            cartItem.quantity -= 1
            cartItem.save()
        else:
            cartItem.delete()
    except Exception as e:
        return HttpResponse(e)
    return redirect('cart')

def RemoveFromCart(request, productId, cartItemId):
    product = get_object_or_404(Product, id = productId)
    
    if request.user.is_authenticated:
        cartItem = CartItem.objects.get(product = product, user = request.user, id = cartItemId)
        
    else:
        cart = Cart.objects.get(cartId = _cartId(request))
        cartItem = CartItem.objects.get(product = product, cart = cart, id = cartItemId)
    
    cartItem.delete()
    
    return redirect('cart')

def ClearCart(request):
    
    cart = Cart.objects.get(cartId = _cartId(request))
    product = get_object_or_404(Product)
    cartItem = CartItem.objects.get(product = product, cart = cart)
    
    cartItem.delete()
    
    return redirect('cart')
        
def CartPage(request, Total = 0, quantity = 0, cartItems = None):
    grandTotal = 0
    shippingCharge = 0
    try:
        
        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user = request.user, isActive = True)
        
        else:
            cart = Cart.objects.get(cartId = _cartId(request))
            cartItems = CartItem.objects.filter(cart = cart, isActive = True)
            
        taxDict = []
        shippingChargeDict = []
        for cartItem in cartItems:
            Total += (cartItem.product.discountedPrice * cartItem.quantity)

            quantity += (cartItem.quantity)

            taxDict.append(cartItem.product.tax)

            shippingChargeDict.append((cartItem.product.shippingCharge))

        # tax = (sum(taxDict)*Total)/100
        shippingCharge = sum(shippingChargeDict)
        shippingCharge = min(shippingCharge, 100)

        grandTotal = Total + shippingCharge

    except ObjectDoesNotExist:
        pass 

    context = {'Total': Total, 'quantity': quantity, 'cartItems': cartItems, 'grandTotal': grandTotal, 'shippingCharge': shippingCharge}


    return render(request, 'store/cart.html', context)

        
@login_required(login_url = 'signin')
def CheckOut(request, Total = 0, quantity = 0, cartItems = None):
    
    grandTotal = 0
    shippingCharge = 0
    try:
        if request.user.is_authenticated:
            cartItems = CartItem.objects.filter(user = request.user, isActive = True)
        
        else:
            cart = Cart.objects.get(cartId = _cartId(request))
            cartItems = CartItem.objects.filter(cart = cart, isActive = True)
            
        taxDict = []
        shippingChargeDict = []
         
        for cartItem in cartItems:
            Total += (cartItem.product.discountedPrice * cartItem.quantity)

            quantity += (cartItem.quantity)

            taxDict.append(cartItem.product.tax)

            shippingChargeDict.append((cartItem.product.shippingCharge))
            
            isCustomizable = cartItem.product.isCustomizable

        # tax = (sum(taxDict)*Total)/100
        shippingCharge = sum(shippingChargeDict)
        shippingCharge = min(shippingCharge, 100)

        grandTotal = Total + shippingCharge
        

    except ObjectDoesNotExist:
        pass 

    context = {'Total': Total, 'quantity': quantity, 'cartItems': cartItems,
               'grandTotal': grandTotal, 'shippingCharge': shippingCharge, 'isCustomizable': isCustomizable}


    
    return render(request, 'store/checkout.html', context)

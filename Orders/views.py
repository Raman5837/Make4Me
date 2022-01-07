from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import datetime
import json

# Verification email

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import requests


from .forms import OrderForm
from .models import Order, Payment, OrderedProduct
from Cart.models import CartItem, Cart
from StoreRoom.models import Product

import razorpay
client = razorpay.Client(auth=("rzp_test_oPffwt6U6JrDNv", "t8cf8bYE21iQUhY6QCH2oVuS"))

# import stripe
# stripe.api_key = settings.STRIPE_PRIVATE_KEY



# Create your views here.

@login_required
def PlaceOrder(request, Total = 0, quantity = 0):
    
    current_user = request.user

    # if the cartCount <= 0 we'll redirect user back to shop.
    cartItems = CartItem.objects.filter(user = current_user)
    cartCount = cartItems.count()

    if cartCount <= 0:
        return redirect('store')

    taxDict = []
    shippingChargeDict = []
    for cartItem in cartItems:
        Total += (cartItem.product.discountedPrice * cartItem.quantity)
        quantity += (cartItem.quantity)
        taxDict.append(cartItem.product.tax)
        shippingChargeDict.append((cartItem.product.shippingCharge))

    global grandTotal
    grandTotal = 0
    shippingCharge = 0

    try:
        tax = (sum(taxDict)*Total)/100
    except ZeroDivisionError:
        tax = 0
    shippingCharge = sum(shippingChargeDict)
    shippingCharge = min(shippingCharge, 100)
    grandTotal = Total + shippingCharge

    if request.method != 'POST':
        return redirect('store')

    form = OrderForm(request.POST, request.FILES)
    try:
        if form.is_valid():
        # Store all of the billing info inside Order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone_number = form.cleaned_data['phone_number']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            data.order_note = form.cleaned_data['order_note']
            data.imageForCustomization1 = form.cleaned_data['imageForCustomization1']
            data.imageForCustomization2 = form.cleaned_data['imageForCustomization2']
            data.paymentMethod = form.cleaned_data['paymentMethod']
            data.orderTotal = grandTotal
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            data.save()

            # Generating Order Number

            year = int(datetime.date.today().strftime('%Y'))
            date = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))

            completeDate = datetime.date(year, month, date)
            currentDate = completeDate.strftime("%Y%m%d")
            global orderNumber
            orderNumber = currentDate + str(data.id)
            data.orderNumber = orderNumber

            data.save()

            order = Order.objects.get(user = current_user, isOrdered = False, orderNumber = orderNumber)

            # RazorPay Starts

            data = {
                'amount': grandTotal*100,
                'currency': 'INR',
                'receipt': orderNumber,
                'payment_capture': '1',
            }
            callbackUrl = 'http://' + str(get_current_site(request))+'/orders/' + 'makePayment/'

            # http://localhost:8000/orders/orderCompletion
            global razorPay
            razorPay = client.order.create(data = data)
            # print('razorPay from placeorder = ',razorPay)
            print('Order ID from razorpay = ',razorPay['id'])
            orderId = razorPay['id']
            global resp
            resp = client.order.fetch(orderId)
            print('razorPay response from PlaceOrder = ',resp)

            # RazorPay Ends


            context = {'order': order, 'cartItems': cartItems, 'Total': Total, 'grandTotal': grandTotal, 'shippingCharge': shippingCharge, 'tax': tax, 'razorPay': razorPay, 'callbackUrl': callbackUrl}

            return render(request, 'orders/payment.html', context)
        else:
            print('Formm is not valid.')
    except Exception as e:
        print('Error --> ', e)


@csrf_exempt
def PaymentView(request):
    
    # print('global resp from Payment view ===> \n',resp)
    # print('taking recipt no. from resp -->', resp['receipt'])
    if request.method == 'POST':
        a = request.POST
        print('a =====>', a)
        try:
            transactionID = request.POST.get('razorpay_payment_id', '')
            orderID = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': orderID,
                'razorpay_payment_id': transactionID,
                'razorpay_signature': signature
            }
            print('content of params_dict ===> \n', params_dict)
            verification = client.utility.verify_payment_signature(params_dict)
            print('verification = ', verification)

        except Exception as e:
            print(e)

        try:
            body = json.loads(request.body)
            order = Order.objects.get(user = request.user, isOrdered = False, orderNumber = body['orderID'])
            print('body--->', body)
        except Exception as e:
            print('error of body',e)

    order = Order.objects.get(user = request.user, isOrdered = False, orderNumber = orderNumber)
    print('global wala orderNumber = ', orderNumber)
    print('orderNumber of Order()', order.orderNumber)
    print('orderId from razorpay', orderID)
    print('orderId from razorpay recipt', resp['receipt'])

    if verification is None:

        try:
            payment = Payment(
                user = request.user,
                paymentId = transactionID,
                paymentMethod = order.paymentMethod,
                amountPaid = order.orderTotal,
                paymentStatus = 'Paid',
                )  
            payment.save()  
        except:
            payment = Payment(paymentStatus = 'Error Occured 😭')
            payment.save()  
    else:
        payment = Payment( paymentStatus = 'Failed')
        payment.save()
    # Storing Transcation Details Inside Payment Model.
    # payment = Payment(
    #     user = request.user,

    #     paymentId = transactionID,
    #     paymentMethod = 'RazorPay',
    #     amountPaid = order.orderTotal,
    #     paymentStatus = resp['status'],

    #     # paymentId = body['transactionID'],
    #     # paymentMethod = body['paymentMethod'],
    #     # amountPaid = order.orderTotal,
    #     # paymentStatus = body['paymentStatus'],
    #     # createdAt = 
    # )
    # payment.save()
    order.payment = payment
    order.isOrdered = True
    order.save()


    # and then we'll move this cart Item in OrderedProduct Table
    cartitem = CartItem.objects.filter(user = request.user)

    for item in cartitem:
        orderedProduct = OrderedProduct()
        orderedProduct.order_id = order.id
        orderedProduct.payment = payment
        orderedProduct.user_id = request.user.id
        orderedProduct.product_id = item.product_id
        orderedProduct.quantity = item.quantity
        orderedProduct.productPrice = item.product.discountedPrice
        orderedProduct.ordered = True
        orderedProduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        productVariant = cart_item.productVariant.all()
        orderedProduct = OrderedProduct.objects.get(id = orderedProduct.id)
        orderedProduct.productVariant.set(productVariant) 

        orderedProduct.save()


        # upto this we've made payment with paypal now we'll reduce sold products quantity
        product = Product.objects.get(id = item.product_id)
        product.inStock -= item.quantity 

        # Here We'll Increase The Sold Count Of The Product
        product.soldCount += item.quantity

        product.save()

    # Then we'll clear the cart
    CartItem.objects.filter(user = request.user).delete()

    # Then we'll send E-mail to customer
    mail_subject = 'Thank You For Your Order'
    message = render_to_string('orders/order_recieved_email.html', {
                'user': request.user,
                'order': order

        })
    email_to = request.user.email
    send_email = EmailMessage(mail_subject, message, to = [email_to])

    send_email.send()


    # then send orderNumber and transactionID back to sendData() Method via JSON Response

    data = {
        'orderNumber': order.orderNumber, 
        'transactionID': payment.paymentId
    }
    try:
        order = Order.objects.get(orderNumber = data['orderNumber'], isOrdered = True)
        orderedProduct = OrderedProduct.objects.filter(order_id = order.id)

        subTotal = sum(i.productPrice * i.quantity for i in orderedProduct)
        payment = Payment.objects.get(paymentId = transactionID)

        context = {'order': order, 'orderedProduct': orderedProduct, 'orderNumber': order.orderNumber, 'transactionID': payment.paymentId, 'payment': payment, 'subTotal': subTotal}

        return render(request, 'orders/orderCompletion.html', context)
    except Exception as e:
        print(e)
        # return render(request, 'orders/orderCompletion.html', context)
        
    # try: 
    #     return JsonResponse(data)
    # except Exception as e:
    #     return HttpResponse(e)
    
                
            
           
def OrderCompleted(request):
    
    if request.GET:
        orderNumber = request.GET.get('orderNumber')
        transactionID = request.GET.get('transactionID')
        
    
    try:
        order = Order.objects.get(orderNumber = orderNumber, isOrdered = True)
        orderedProduct = OrderedProduct.objects.filter(order_id = order.id)
        payment = Payment.objects.get(paymentId = transactionID)
        
        sub_total = orderedProduct.quantity * orderedProduct.productPrice
        
        
        
        context = {'order': order, 'orderedProduct': orderedProduct, 'orderNumber': order.orderNumber, 'transactionID': payment.paymentId, 'payment': payment, 'sub_total': sub_total}
        
        return render(request, 'orders/orderCompletion.html', context)
    
    # except (Payment.DoesNotExist, Order.DoesNotExist):
    except:
        return render(request, 'orders/orderCompletion.html')
        # return redirect('home')
       

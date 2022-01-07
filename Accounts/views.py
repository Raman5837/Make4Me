from django.contrib import messages, auth
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests

from .forms import SignupForm, UserAccountForm, UserProfileForm
from .models import Account, UserProfile
from Cart.models import Cart, CartItem
from Cart.views import _cartId
from Orders.models import Order, OrderedProduct
# Create your views here.


def Signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)

            user.gender = gender
            user.phone_number = phone_number

            user.save()

            # Creating User Profile
            userProfile = UserProfile()
            userProfile.user_id = user.id
            userProfile.profilePicture = 'Images/Default/user.png'
            userProfile.save()

            # USER ACTIVATION
            # sending activation link to user email address , to activate the account.
            # getting location of current site

            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Make4Me Account'
            message = render_to_string('accounts/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_to = email
            send_email = EmailMessage(mail_subject, message, to=[email_to])
            send_email.send()

            # messages.success(request, "Thank You For Creating Account. We've Sent You An Verification E-mail, Please Verify Your Account To Login.")
            return redirect('/accounts/signin/?command=verification&email='+email)

    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


def Signin(request):  # sourcery no-metrics

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                # here we'll check if there is any cartItem before user logged in . if it exist we'll show it in cart after user login.

                cart = Cart.objects.get(cartId=_cartId(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()

                if is_cart_item_exists:
                    cartItem = CartItem.objects.filter(cart=cart)

                    # grouping the existing product together.
                    product_variation = []
                    for item in cartItem:
                        variation = item.productVariant.all()
                        product_variation.append(list(variation))

                    # getting cart items for the user to access it's product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.productVariant.all()

                        existing_variation_List = list(existing_variation)
                        ex_var_list.append(existing_variation_List)
                        id.append(item.id)

                    for pv in product_variation:
                        if pv in ex_var_list:
                            index = ex_var_list.index(pv)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()

                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            # it'll hold previous url from where we've came here(at the page)
            url = request.META.get('HTTP_REFERER')

            try:
                query = requests.utils.urlparse(url).query
                # next=/x/y/ . we've to split it
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('signin')

    return render(request, 'accounts/signin.html')


@login_required(login_url='signin')
def Logout(request):
    auth.logout(request)
    messages.success(request, 'Logout Successfully ')
    return redirect('signin')


def Activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        messages.success(
            request, 'Congratulations! Your Account Has Been Activated')

        return redirect('signin')

    else:
        messages.success(request, 'Invalid Activation Link. Try Again')
        return redirect(request, 'signup')


@login_required(login_url='signin')
def Dashboard(request):

    orders = Order.objects.order_by(
        '-createdAt').filter(user_id=request.user.id, isOrdered=True)
    orderCount = orders.count()

    userProfile = UserProfile.objects.get(user_id=request.user.id)

    context = {'orderCount': orderCount,
               'userProfile': userProfile, 'orders': orders}
    return render(request, 'accounts/dashboard.html', context)


def ForgotPassword(request):

    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():

            user = Account.objects.get(email__exact=email)

            # sending password-reset email to the user
            current_site = get_current_site(request)
            mail_subject = 'Make4Me | Password Reset'
            message = render_to_string('accounts/reset_password_validate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email_to = email
            send_email = EmailMessage(mail_subject, message, to=[email_to])
            send_email.send()

            messages.success(
                request, 'Password Reset E-mail Has Been Sent To Your E-mail Address.')
            return redirect('signin')

        else:
            messages.error(request, "Account Does Not Exist.")
            return redirect('forgotPassword')

    return render(request, 'accounts/forgot_password.html')


def ResetPassword_Validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please Reset Your Password')

        return redirect('resetPassword')

    else:
        messages.error(
            request, 'Password Reset Link Has Been Expired, Try Again')
        return redirect('forgotPassword')


def ResetPassword(request):

    if request.method != 'POST':
        return render(request, 'accounts/resetPassword.html')
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']

    if len(password) < 8:
        messages.error(request, 'Password Must Be At Least 8 Characters')
        return redirect('resetPassword')

    if password == confirmPassword:

        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        user.set_password(password)

        user.save()
        messages.success(request, 'Password Reset Successfully')
        return redirect('signin')

    else:
        messages.error(
            request, 'Password and Confirm Password Does Not Match')
        return redirect('resetPassword')


@login_required(login_url='signin')
def ViewMyOrders(request, orderID):

    orderDetail = OrderedProduct.objects.filter(order__orderNumber=orderID)
    orders = Order.objects.get(orderNumber=orderID)

    subTotal = sum(i.productPrice * i.quantity for i in orderDetail)
    quantity = sum(i.quantity for i in orderDetail)
    shippingCharge = orders.orderTotal - subTotal
    context = {'orderDetail': orderDetail, 'orders': orders, 'subTotal': subTotal,
               'quantity': quantity, 'shippingCharge': shippingCharge}

    return render(request, 'accounts/manageOrders.html', context)


@login_required(login_url='signin')
def MyOrders(request):

    orders = Order.objects.filter(
        user=request.user, isOrdered=True).order_by('-createdAt')
    # orderedProduct = OrderedProduct.objects.filter(user = request.user, ordered = True).order_by('-createdAt')

    context = {'orders': orders, }

    return render(request, 'accounts/myOrders.html', context)


@login_required(login_url='signin')
def EditUserProfile(request):

    userProfile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        userForm = UserAccountForm(request.POST, instance=request.user)
        profileForm = UserProfileForm(
            request.POST, request.FILES, instance=userProfile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()

            messages.success(request, 'Your Profile Has Been Updated')
            return redirect('MyProfile')

    else:
        userForm = UserAccountForm(instance=request.user)
        profileForm = UserProfileForm(instance=userProfile)

    context = {'userForm': userForm,
               'profileForm': profileForm, 'userProfile': userProfile}

    return render(request, 'accounts/editProfile.html', context)


@login_required(login_url='signin')
def ViewUserProfile(request):
    return render(request, 'accounts/myProfile.html')


@login_required(login_url='signin')
def ChangePassword(request):

    if request.method == 'POST':

        currentPassword = request.POST['currentPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']

        user = Account.objects.get(username__exact=request.user.username)

        if newPassword == confirmPassword:
            success = user.check_password(currentPassword)
            if success:
                user.set_password(newPassword)
                user.save()
                auth.logout(request)
                messages.success(request, 'Password Updated Successfully')
                return redirect('dashboard')
            else:
                messages.error(request, 'Enter Valid Current Password')
        else:
            messages.error(
                request, 'Your New Password And Confirm Password Are Not Matching.')
            return redirect('changePassword')

    return render(request, 'accounts/changePassword.html')

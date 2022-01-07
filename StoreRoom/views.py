from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, ProductGallery, ReviewAndRating
from .forms import ReviewForm
from Category.models import Category
from Cart.models import CartItem
from Cart.views import _cartId
from Orders.models import OrderedProduct
# Create your views here.

def Store(request, categorySlug = None):
    
    categories = None
    products = None

    if categorySlug is not None:
        categories = get_object_or_404(Category, slug = categorySlug)
        products = Product.objects.filter(category = categories, isAvailable = True).order_by('id')
    else:
        products = Product.objects.all().filter(isAvailable = True).order_by('id')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    productsInPage = paginator.get_page(page)

    productCount = products.count()



    context = {'products': productsInPage, 'productCount': productCount,}
    return render(request, 'store/store.html', context)

# Product Detail View
def ProductDetail(request, categorySlug, productSlug):
    
    try:
        singleProduct = Product.objects.get(category__slug = categorySlug, slug = productSlug)
        inCart = CartItem.objects.filter(cart__cartId = _cartId(request), product = singleProduct).exists()
        # it'll return True if the product is already in the cart , else it'll return False
    except Exception as err:
        raise err
    
    if request.user.is_authenticated:
        try:
            orderedProduct = OrderedProduct.objects.filter(user = request.user, product_id = singleProduct.id).exists()
        except OrderedProduct.DoesNotExist:
            orderedProduct = None
    else:
        orderedProduct = None
              
    # Getting Reviews
    reviews = ReviewAndRating.objects.filter(product_id = singleProduct.id, status = True)
    
    productGallery = ProductGallery.objects.filter(product_id = singleProduct.id)
    
    difference = singleProduct.highPrice - singleProduct.discountedPrice
    percentage = (difference / singleProduct.highPrice) 
    discountPercent = str(round(percentage * 100, )) + ' % OFF'
    
    
    # Related Products
    relatedProducts = Product.objects.filter(category = singleProduct.category).exclude(id = singleProduct.id)[:6]
    
    
    context = {'singleProduct': singleProduct, 'inCart': inCart, 'orderedProduct': orderedProduct, 'reviews': reviews, 'productGallery': productGallery, 'discountPercent': discountPercent, 'relatedProducts': relatedProducts}
    
    return render(request, 'store/product_detail.html', context)


# For searching products using search bar.
def SearchProducts(request):
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            
            products = Product.objects.order_by('-create_at').filter(Q(productName__icontains = keyword) or Q(description__icontains = keyword) or Q(details__icontains = keyword) or Q(keywords__icontains = keyword))
            productCount = products.count()
    context = {'products': products, 'productCount': productCount}
    
    return render(request, 'store/store.html', context)

def ReviewProduct(request, productID):
    
    currentUrl = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        try:
            
            reviews = ReviewAndRating.objects.get(user__id = request.user.id, product__id = productID)
            form = ReviewForm(request.POST, instance = reviews)
            form.save()
            messages.success(request, 'Thank You ! Your Review Has Been Updated')
            
            return redirect(currentUrl)
            
        except ReviewAndRating.DoesNotExist:
            
            form = ReviewForm(request.POST)
            
            if form.is_valid():
                data = ReviewAndRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = productID
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank You ! Your Review Has Been Submitted')
                return redirect(currentUrl)
                 
            
            
            
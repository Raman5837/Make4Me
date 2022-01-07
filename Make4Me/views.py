from django.shortcuts import render
from django.db.models import Q
from StoreRoom.models import Product, ReviewAndRating, Slider
from Category.models import Category


def Home(request):
    products = Product.objects.all().filter(isAvailable=True).order_by('-create_at')
    category = Category.objects.all()

    mensProduct = Category.objects.all().filter(
        categoryName__iexact="Men's Clothing")
    womensProduct = Category.objects.all().filter(
        categoryName__iexact="Women's Clothing")
    GiftItems = Category.objects.all().filter(categoryName__iexact="Gift & Decor")

    recentProducts = Product.objects.all().filter(
        label='New', isAvailable=True).order_by('-modified_at')[:8]

    bestSellers_inFashion = Product.objects.filter(Q(category__categoryName__icontains="Men's Clothing") or Q(category__categoryName__icontains="Women's Clothing") or Q(
        keywords__icontains="Men's Fashion") or Q(keywords__icontains="Women's Fashion") or Q(keywords__icontains="Fashion"), isAvailable=True).order_by('-soldCount')[:8]

    bestSellers_inGiftItems = Product.objects.filter(Q(category__categoryName__icontains="Gift & Decor") or Q(category__categoryName__icontains="Gifts Item") or Q(
        keywords__icontains="Gift Items") or Q(keywords__icontains="Gifts"), isAvailable=True).order_by('-soldCount')[:8]

    bestSellers_inPersonalCare = Product.objects.filter(Q(category__categoryName__icontains="Personal Care") or Q(
        category__categoryName__icontains="Hygiene") or Q(keywords__icontains="Personal Care And Hygiene"), isAvailable=True).order_by('-soldCount')[:8]

    bestSellers_inAccessories = Product.objects.filter(Q(category__categoryName__icontains="Accessories") or Q(category__categoryName__icontains="Men's Accessories") or Q(
        category__categoryName__icontains="Women's Accessories") or Q(keywords__icontains="Accessories"), isAvailable=True).order_by('-soldCount')[:8]

    make4meSpecial = Product.objects.filter(
        label='Make4Me Special').order_by('-modified_at')[:4]
    forSale = Product.objects.filter(label='Sale').order_by('-modified_at')[:4]
    promotionalProduct = Product.objects.filter(
        label='Promotion').order_by('-modified_at')[:4]

    slider = Slider.objects.all().filter(isActive=True)

    # Getting the review
    reviews = None
    for product in products:
        reviews = ReviewAndRating.objects.filter(
            product_id=product.id, status=True)

    context = {'products': products, 'reviews': reviews, 'category': category, 'mensProduct': mensProduct, 'womensProduct': womensProduct, 'GiftItems': GiftItems, 'recentProducts': recentProducts, 'bestSellers_inFashion': bestSellers_inFashion,
               'bestSellers_inGiftItems': bestSellers_inGiftItems, 'bestSellers_inPersonalCare': bestSellers_inPersonalCare, 'bestSellers_inAccessories': bestSellers_inAccessories, 'make4meSpecial': make4meSpecial, 'forSale': forSale, 'promotionalProduct': promotionalProduct, 'slider': slider}
    return render(request, 'home.html', context)

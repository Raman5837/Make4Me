from django.urls import path
from . import views
urlpatterns = [
    path('', views.Store, name = 'store'),
    path('category/<slug:categorySlug>/', views.Store, name = 'productByCategory'),
    path('category/<slug:categorySlug>/<slug:productSlug>/', views.ProductDetail, name = 'productDetail'),
    path('searchProducts/', views.SearchProducts, name = 'searchProducts'),
    path('rateProduct/<int:productID>/', views.ReviewProduct, name = 'rateProduct'),
]
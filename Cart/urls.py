from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.CartPage, name = 'cart'),
    path('addToCart/<int:productId>/', views.AddToCart, name = 'addToCart'),
    path('decreaseQuantity/<int:productId>/<int:cartItemId>/', views.DecreaseQuantity, name = 'decreaseQuantity'),
    path('removeFromCart/<int:productId>/<int:cartItemId>/', views.RemoveFromCart, name = 'removeFromCart'),
    path('checkout/', views.CheckOut, name = 'checkout'),
    
    path('clearCart/', views.ClearCart, name = 'clearCart'),
]
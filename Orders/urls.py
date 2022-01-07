from django.urls import path
from . import views

urlpatterns = [
    
    path('placeOrder/', views.PlaceOrder, name = 'placeOrder'),
    path('makePayment/', views.PaymentView, name = 'makePayment'),
    path('orderCompletion/', views.OrderCompleted, name = 'orderCompletion'),
    
]
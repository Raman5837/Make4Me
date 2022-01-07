from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.Dashboard, name = 'dashboard'),
    path('signup/', views.Signup, name = 'signup'),
    path('signin/', views.Signin, name = 'signin'),
    path('logout/', views.Logout, name = 'logout'),
    path('dashboard/', views.Dashboard, name = 'dashboard'),
    
    path('activate/<uidb64>/<token>/', views.Activate, name = 'activate'),
    path('resetPassword_validate/<uidb64>/<token>/', views.ResetPassword_Validate, name = 'resetPassword_validate'),
    
    path('forgotPassword/', views.ForgotPassword, name = 'forgotPassword'),
    path('resetPassword/', views.ResetPassword, name = 'resetPassword'),
    
    path('myOrders/', views.MyOrders, name = 'myOrders'),
    path('viewMyOrders/<int:orderID>/', views.ViewMyOrders, name = 'viewMyOrders'),
    path('editMyProfile/', views.EditUserProfile, name = 'editMyProfile'),
    path('MyProfile/', views.ViewUserProfile, name = 'MyProfile'),
    path('changePassword/', views.ChangePassword, name = 'changePassword'),
    
]
"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from.import views

urlpatterns = [
    path('', views.home,  name ='home'),
    path('login/',views.login, name ='login'),
    path('signup/',views.signup, name ='signup'),
    path('homeuser/',views.homeuser, name ='homeuser'),
    path('userlogout/',views.userlogout, name = 'userlogout'),
    path('productdetails/<int:id>/',views.productdetails, name = 'productdetails'),
    path('categoryproducts/<int:id>/',views.categoryproducts, name = 'categoryproducts'),
    path('addcart/<int:id>/',views.addcart, name = 'addcart'),
    path('showcart/',views.showcart, name = 'showcart'),
    path('count/<int:id>/',views.count, name = 'count'),
    path('cartdelete/<int:id>/',views.cartdelete, name = 'cartdelete'),
    path('addressadd/',views.addressadd, name = 'addressadd'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('addressremove/<int:id>/',views.addressremove, name= 'addressremove'),
    path('buynow/<int:id>/',views.buynow, name= 'buynow'),
    path('selectaddress/<int:id>/',views.selectaddress, name = 'selectaddress'),
    path('placeorder/',views.placeorder, name = 'placeorder'),
    path('cod/',views.cod,name = 'cod'),
    path('paypal/',views.paypal, name = 'paypal'),
    path('payrazor/',views.payrazor, name = 'payrazor'),
    path('paypalrazor/<int:id>/',views.paypalrazor, name = 'paypalrazor'),
    path('userprofile/',views.userprofile, name = 'userprofile'),
    path('edituser/<int:id>/', views.edituser, name = 'edituser'),
    path('changepassword/<int:id>/', views.changepassword, name = 'changepassword'),
    path('loginwithphone/',views.loginwithphone,name = 'loginwithphone'),
    path('otpconfirmation/',views.otpconfirmation,name = 'otpconfirmation'),
    path('successpayment/',views.successpayment,name = 'successpayment'),
    path('product_search/',views.product_search, name = 'product_search'),
    path('search_show/',views.search_show, name = 'search_show'),
    path('order_cancel/<int:id>/',views.order_cancel, name = 'order_cancel'),
    # path('payrazor',views.payrazor, name='payrazor'),

    
]
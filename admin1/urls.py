from django.urls import path
from.import views

urlpatterns = [
    path('', views.adhome,  name ='adhome'),
    path('adlogin/',views.adlogin, name ='adlogin'),
    path('adminuser/',views.adminuser, name ='adminuser'),
    path('adminuserdelete/<int:id>/',views.adminuserdelete, name ='adminuserdelete'),
    path('adminuserblock/<int:id>/',views.adminuserblock, name = 'adminuserblock'),
    path('adminproductcategory/',views.adminproductcategory, name = 'adminproductcategory'),
    path('adminproductadd/',views.adminproductadd, name = 'adminproductadd'),
    path('adminaddproductcategory/',views.adminaddproductcategory, name = 'adminaddproductcategory'),
    path('category_delete/<int:id>/',views.category_delete, name = 'category_delete'),
    path('adminproductview/',views.adminproductview, name ='adminproductview'),
    path('productdelete/<int:id>/',views.productdelete, name = 'productdelete'),
    path('productedit/<int:id>/',views.productedit, name = 'productedit'),
    path('adminlogout/' ,views.adminlogout, name = 'adminlogout'),
    path('adminorderlist/',views.adminorderlist, name = 'adminorderlist'),
    path('statusedit/<int:id>/',views.statusedit, name = 'statusedit'),
    path('adminreport/',views.adminreport, name = 'adminreport'),
    path('reportfilter/',views.reportfilter,name = 'reportfilter'),
    path('excel_export/',views.excel_export, name = 'excel_export'),
    path('discount/<int:id>/',views.discount, name = 'discount'),
    path('discount_remove/<int:id>/',views.discount_remove, name = 'discount_remove'),
    path('admincoupon/',views.admincoupon, name = 'admincoupon'),
    path('couponedit/<int:id>/',views.couponedit, name = 'couponedit'),
    path('coupon_status/<int:id>/',views.coupon_status, name = 'coupon_status'),
  
    # path('signup/',views.signup, name ='signup'),
]
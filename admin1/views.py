from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User,auth
from user.models import MyUsers,UserCart,AddressTable,Order
from .models import Categories,ProductDetails,Coupon
from django.core.files import File
import base64
from django.core.files.base import ContentFile
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from datetime import datetime
import xlwt
from django.contrib import messages

# Create your views here.
search_report = 0
def adhome(request):
    if request.session.has_key('adkey'):
        return redirect(adlogin)
    else:
        return render(request, 'admintemp/login.html')



def adlogin(request):
    if request.session.has_key('adkey'):
        today_date = date.today()
        month_ago = today_date - relativedelta(months =1)
        year_ago = today_date - relativedelta(years =1)
        week_ago = today_date - relativedelta(weeks =1)
        print(month_ago, 'heyyyyyy')
        last_month_orders = Order.objects.filter(date__range = [month_ago, today_date]) 
        last_year_orders = Order.objects.filter(date__range = [year_ago, today_date])
        last_week_orders = Order.objects.filter(date__range = [week_ago, today_date])
        today_orders = Order.objects.filter(date=today_date)
        total_orders = Order.objects.all().count()
        pending_orders = Order.objects.filter(~Q(status='delivered')).count()
        user_count = User.objects.all().count()
        product_count = ProductDetails.objects.count()
        month_revennue=0
        for order in last_month_orders:
            month_revennue = month_revennue + (order.count * order.price)
        year_revennue = 0
        for order in last_year_orders:
            year_revennue = year_revennue + (order.count * order.price )
        week_revennue = 0
        for order in last_week_orders:
            week_revennue = week_revennue + (order.count * order.price)
        today_revennue = 0
        for order in today_orders:
            today_revennue = today_revennue + (order.count * order.price)
        context = {'m_revennue':month_revennue , 'y_revennue':year_revennue,'w_revennue':week_revennue,'t_revennue':today_revennue,'total_count':total_orders,'pending_count':pending_orders,'user_count':user_count,'product_count':product_count}    
        return render(request, 'admintemp/index.html',context) 
    
    elif request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        if (username=='admin' and password=='123'):
            request.session['adkey'] ='admin'  
            return JsonResponse('true', safe=False)
        else :
            return JsonResponse('false', safe=False)
    
    else:
        return redirect(adhome)
         
    
          

def adminuser(request):
   if request.session.has_key('adkey'):
       user_records = MyUsers.objects.all()
       return render(request, 'admintemp/usertable.html' , {'datas':user_records})
   else:
       return redirect(adhome)
def adminuserdelete(request,id):
    print('idddddd',id)
    current_user = MyUsers.objects.get(user_id=id)
    current_user1 = User.objects.get(id=current_user.user_id)
    current_user.delete()
    current_user1.delete()
    
    # current_user1 = User.objects.all(id1=id)
    # current_user1.delete()
    # user_records = MyUsers.objects.all()
    # return render(request, 'admintemp/usertable.html' , {'datas':user_records})
    return redirect(adminuser)
def adminuserblock(request,id):
    user = User.objects.get(id=id)
    current_user = MyUsers.objects.get(user=user)
   
    if user.is_active==False:
        user.is_active=True
    else:
        user.is_active=False
    user.save()
    return redirect(adminuser)
def adminproductview(request):
    if request.session.has_key('adkey'):
        products =ProductDetails.objects.all()
        return render(request,'admintemp/productview.html',{'products':products})
    else:
        return redirect(adhome)


def adminproductadd(request):
    if request.method == 'POST':
        product_name=request.POST['name']
        category=request.POST['category']
        weight=request.POST['weight']
        price=request.POST['price']
        discription=request.POST['discription']
        print(type(weight))
        print(type(price))
        if product_name == '' or category == '' or weight == '' or price == '' or discription == '':
            messages.info(request,'add every details properly')
            return redirect(adminproductadd)
        else:  
            image1 = request.POST['imageurl1']
            image2 = request.POST['imageurl2']
            image3 = request.POST['imageurl3']
            if image1=='' or image2 =='' or image3 =='':
                messages.info(request,'crop every image properly')
                return redirect(adminproductadd)
            else:
                format, imgstr = image1.split(';base64,')
                ext = format.split('/')[-1]
                img1 = ContentFile(base64.b64decode(imgstr),name=product_name+ '.' + ext)
            
                format, imgstr2 = image2.split(';base64,')
                ext2 = format.split('/')[-1]
                img2 = ContentFile(base64.b64decode(imgstr2),name=product_name+ '.' + ext2)
                
                format, imgstr3 = image3.split(';base64,')
                ext3 = format.split('/')[-1]
                img3 = ContentFile(base64.b64decode(imgstr3),name=product_name+ '.' + ext3)
                

                category = Categories.objects.get(category= category)
                current_product= ProductDetails.objects.create(name=product_name, weight=weight, price=price, category_name=category, discription=discription,image1=img1,image2=img2,image3=img3)
                current_product.save() 
                return redirect(adminproductview)
        # return JsonResponse('true' , safe=False)  
        # else:
        #     return JsonResponse('false', safe=False)   
    
    else:
        category_object = Categories.objects.all()
        return render(request, 'admintemp/register.html',{'category':category_object})
    
def adminproductcategory(request):
    if request.session.has_key('adkey'):
        category_object = Categories.objects.all()
        return render(request, 'admintemp/category.html', {'category':category_object} )
    else:
        return redirect(adhome)

def adminaddproductcategory(request):
    if request.method == 'POST':
        category =request.POST['category']
        Categories.objects.create(category=category)
        category_object = Categories.objects.all()
        return render(request, 'admintemp/category.html', {'category':category_object} )
    else:
        return render(request, 'admintemp/categoryadd.html')
def category_delete(request,id):
    category = Categories.objects.get(id=id)
    category.delete()
    return redirect(adminproductcategory)
def discount_remove(request,id):
    category = Categories.objects.get(id=id)
    category.discount = 0
    category.save()
    return redirect(adminproductcategory)
def productdelete(request,id):
    product = ProductDetails.objects.get(id=id)
    product.delete()
    return redirect(adminproductview)
def productedit(request,id):
    product = ProductDetails.objects.get(id=id)
    category = Categories.objects.all()
    context ={'products':product , 'categories':category}
    if request.method== 'POST':
        name = request.POST['name']
        weight = request.POST['weight']
        price = request.POST['price']
        discription = request.POST['discription']
        category = request.POST['category']
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        category1 = Categories.objects.get(category=category)
        
        product.name = name
        product.weight = weight
        product.price = price
        product.discription = discription
        product.category_name = category1
        if image1 == None:
            pass
        else:
            product.image1 = image1
        if image2 == None:
            pass
        else:
            product.image2 = image2
        if image3 == None:
            pass
        else:
            product.image3 = image3
        product.save()

        return redirect(adminproductview)




    else:
        return render(request, 'admintemp/productedit.html',context)

def adminorderlist(request):
    print('trueeee')
    order = Order.objects.all()
    stat = ['ordered','shipped','delivered']
    return render(request, 'admintemp/orderlist.html',{'order':order,'stat':stat})
def statusedit(request,id):
    print('hello')
    order = Order.objects.get(id=id) 
    order.status = request.POST['stat1']
    order.save()
    print(order.status)
    return JsonResponse('true',safe=False)

def adminreport(request):
    if request.method == 'POST': 
        f_date = request.POST['f_date']
        t_date = request.POST['t_date']
        request.session['f_date'] = f_date
        request.session['t_date'] = t_date
        global search_report
        search_report = Order.objects.filter(date__range = [f_date,t_date])
        return JsonResponse('true', safe=False)
    else:     
        orders = Order.objects.all()
        context = {'orders':orders}
        if request.session.has_key('f_date'):
            del request.session['f_date']
            del request.session['t_date']
        return render(request,'admintemp/report.html',context)

def reportfilter(request):
    global search_report
    print(search_report, 'dsda')
    context = {'orders':search_report}
    return render(request,'admintemp/report.html',context)

def excel_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product', 'User', 'Price(per unit)', 'Quantity','order_date','order_status' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
   
    if request.session.has_key('f_date'):
        f_date = request.session['f_date']
        t_date = request.session['t_date']
        rows = Order.objects.filter(date__range =[f_date,t_date]).values_list('product__name', 'user__user__username', 'price', 'count', 'date','status')   

    else: 
        rows = Order.objects.all().values_list('product__name', 'user__user__username', 'price', 'count', 'date','status')
         
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response
def discount(request,id):
    print(id)  
    if request.method=='POST':
        discount = request.POST['discount']
        category = Categories.objects.get(id=id)
        category.discount = discount
        category.save()
        print('heklo')
        return JsonResponse('true', safe=False )
def admincoupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        off = int(request.POST['off'])
        Coupon.objects.create(code=code,off=off)
        return redirect(admincoupon)
    else:
        coupon = Coupon.objects.all()
        return render(request,'admintemp/coupon.html',{'coupon':coupon})
def couponedit(request,id):
    if request.method == 'POST':
        coupon = Coupon.objects.get(id=id)
        coupon.code = request.POST['code']
        coupon.off = request.POST['off']
        coupon.save()
        return JsonResponse('true',safe=False)
    else:
        print('pooda')
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        return JsonResponse('true1',safe=False)
def coupon_status(request,id):
    coupon = Coupon.objects.get(id=id)
    if coupon.status==True:
        coupon.status = False
        coupon.save()
        return JsonResponse('true', safe=False)
    else:
        coupon.status = True
        coupon.save()
        return JsonResponse('true', safe=False)
def adminlogout(request):
    request.session.flush()
    return redirect(adhome)
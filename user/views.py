from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.http import JsonResponse 
from .models import MyUsers,UserCart,AddressTable,Order
from admin1.models import ProductDetails,Categories,Coupon
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import random
from twilio.rest import Client
import uuid


# Create your views here.
phone_number=0
otp=0
g1total=0
def home(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect(homeuser)     
    else:
        products = ProductDetails.objects.all()
        category = Categories.objects.all()
        context = {'products':products ,'category':category}
        return render(request, 'home.html' ,context) 
def login(request): 
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_active == True:
                user =auth.authenticate(username=username,password=password)
                if user is not None:
                    auth.login(request,user)
                    return JsonResponse('true', safe=False)
                else :
                    return JsonResponse('false', safe=False)
            else:
                return JsonResponse('block', safe=False)
        else:
            return JsonResponse('false', safe=False)
    else :
        category = Categories.objects.all()
        return render(request, 'login.html',{'category':category})
def signup(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        password2=request.POST['password2']
        referral_code = request.POST['referral'] 
        
        if password==password2:
            code = str(uuid.uuid4())[:12]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            
            if referral_code != '':
                try:
                    recommented_myuser = MyUsers.objects.get(referral_code=referral_code)
                except:
                    return JsonResponse('true1',safe=False) 
                recommented_myuser = MyUsers.objects.get(referral_code=referral_code)
                recommented_user = User.objects.get(id=recommented_myuser.user_id)
                MyUsers.objects.create(user=user,phone_number=phone_number,referral_code=code,recommended_by=recommented_user)
                recommented_myuser.referral_earnings = 30
                recommented_myuser.save() 
                current_user = MyUsers.objects.get(referral_code=code)
                current_user.referral_earnings = 15
                current_user.save()        
            else:   
                MyUsers.objects.create(user=user,phone_number=phone_number,referral_code=code) 
                current_user = MyUsers.objects.get(referral_code=code)
                current_user.referral_earnings = 15
                current_user.save()
            return JsonResponse('true' , safe=False)  
        else:
            return JsonResponse('false', safe=False)   

def homeuser(request):
    if request.user.is_active == True:
        products = ProductDetails.objects.all()
        category = Categories.objects.all()
        context = {'products':products ,'category':category}
        return render(request,'homeuser.html',context)
    else:
        return redirect(home)
def productdetails(request,id):
    productdetails = ProductDetails.objects.get(id=id)
    category = Categories.objects.all()
    context = {'product': productdetails, 'category':category}
    return render(request, 'productdetails.html', context)
def categoryproducts(request,id):
    cat = Categories.objects.get(id=id)
    products = ProductDetails.objects.filter(category_name=cat)
    category = Categories.objects.all()
    context = {'products':products,'category':category}
    return render(request, 'categoryproducts.html', context)
def addcart(request,id): 
    try:
        current_user = MyUsers.objects.get(user_id=request.user.id)
        cart_product = ProductDetails.objects.get(id=id)
        UserCart.objects.create(user=current_user,product=cart_product)
        return redirect(homeuser)
    except:
        return redirect(login)
def showcart(request):
    try:
        current_user  = User.objects.get(id=request.user.id)
        current_myuser = MyUsers.objects.get(user=current_user)  
        if  UserCart.objects.filter(user=current_myuser).exists():
            current_usercart = UserCart.objects.filter(user=current_myuser).order_by('date')
            category = Categories.objects.all()
            grandtotal=0
            for j in current_usercart:
                product2 = ProductDetails.objects.get(id=j.product_id)             
                if product2.category_name.discount == 0:
                    grandtotal = grandtotal + float(product2.price)*j.count
                else:
                    grandtotal = grandtotal + float(product2.discount_price)*j.count
            context = {'current_usercart':current_usercart ,'grandtotal':grandtotal , 'category':category}
            return render (request, 'usercart.html',context)
           
        else:
           
             return render(request, 'usercartempty.html')
    except:
        return redirect(login)

@csrf_exempt 
def count(request,id):
    if request.method == 'GET':
        action = request.GET['action']
        cart_field = UserCart.objects.get(id=id)
        if action == 'plus':
            cart_field.count += 1 
        else:
            if cart_field.count != 1:
                cart_field.count -= 1
            else:
                pass
        cart_field.save()
        return JsonResponse('true',safe=False)
def cartdelete(request,id):
    current_cart = UserCart.objects.get(id=id) 
    current_cart.delete()
    return JsonResponse('true', safe=False)
def addressadd(request):
    if request.method == 'POST':
        housename = request.POST['housename']
        street = request.POST['street']
        city = request.POST['city']
        district = request.POST['district']
        state = request.POST['state']
        pincode =  request.POST['pincode']
        current_user2 = User.objects.get(id=request.user.id)
        current_myuser2 = MyUsers.objects.get(user= current_user2)
        AddressTable.objects.create(housename=housename,street=street,city=city,district=district,state=state,pincode=pincode,user=current_myuser2)
        return redirect (checkout)
    else:
        return render(request, 'addressadd.html')

def checkout(request):
    current_user = User.objects.get(id=request.user.id)
    current_myuser = MyUsers.objects.get(user= current_user) 
    current_address = AddressTable.objects.filter(user=current_myuser)
    current_usercart = UserCart.objects.filter(user=current_myuser)
    category = Categories.objects.all()
    grandtotal=0
    for j in current_usercart:
        product2 = ProductDetails.objects.get(id=j.product_id)
        if product2.category_name.discount == 0:
            grandtotal = grandtotal + float(product2.price)*j.count
        else:
            grandtotal = grandtotal + float(product2.discount_price)*j.count
    referral_earnings = current_myuser.referral_earnings
    if current_myuser.referral_earnings != 0:
        total = float(grandtotal-referral_earnings)
        context = {'current_usercart':current_usercart , 'address':current_address ,'grandtotal':grandtotal , 'category':category ,'total':total,'ref_earnings':referral_earnings}
        request.session['grandtotal'] = total
        return render(request, 'checkout.html' , context )
    else:
        context = {'current_usercart':current_usercart , 'address':current_address ,'grandtotal':grandtotal , 'category':category,'ref_earnings':referral_earnings }
        request.session['grandtotal'] = grandtotal
        return render(request, 'checkout.html' , context )

def addressremove(request,id):
    remove_address = AddressTable.objects.get(id=id)
    remove_address.delete()
    return JsonResponse('true',safe=False)  
def buynow(request,id):
    try:
        current_user = MyUsers.objects.get(user_id=request.user.id)
    except:
        return redirect(login)
    cart_product = ProductDetails.objects.get(id=id)
    UserCart.objects.create(user=current_user,product=cart_product)
    return redirect(checkout)
def selectaddress(request,id):
    request.session['id']=id
    return JsonResponse('data' ,safe=False)

def placeorder(request):
    coupon_code = request.GET['coupon_code']
    if coupon_code != '': 
        if Coupon.objects.filter(code=coupon_code).exists():
            coupon = Coupon.objects.get(code=coupon_code)
            request.session['coupon_off'] = coupon.off
    
    if request.GET['v'] == 'cod':
        return JsonResponse('true', safe=False)
    elif  request.GET['v'] =='paypal':
        return JsonResponse('true2',safe=False)
    elif  request.GET['v'] =='razorpay':
        return JsonResponse('true3', safe=False)
   
def cod(request):
    try:
        add_id = request.session['id']
    except:
        messages.info(request,'please select an address')
        return redirect(checkout)
    opted_address = AddressTable.objects.get(id=add_id)
    cart = UserCart.objects.filter(user=opted_address.user.user_id)

    if request.session.has_key('coupon_off'):
        coupon_off = request.session['coupon_off']
    else:
        coupon_off = 0

    for i in cart:
        if i.product.category_name == 0:   
            total_price = (i.count*i.product.price) - coupon_off   
            Order.objects.create(user=i.user,product=i.product,address=opted_address,status='ordered',count=i.count,price=total_price,payment_method='COD')
            i.delete()
            coupon_off = 0
        else:
            total_price = (i.count*float(i.product.discount_price)) - coupon_off
            Order.objects.create(user=i.user,product=i.product,address=opted_address,status='ordered',count=i.count,price=total_price,payment_method='COD')
            i.delete()
            coupon_off = 0

    if request.session.has_key("coupon_off"):
        del request.session['coupon_off']   
     
    del request.session['id']
    current_user  = User.objects.get(id=request.user.id)
    current_myuser = MyUsers.objects.get(user=current_user)
    current_myuser.referral_earnings = 0
    current_myuser.save()
    return render(request,'successpage.html')

def paypal(request):
    try:
        add_id = request.session['id']
    except:
        messages.info(request,'please select an address')
        return redirect(checkout)
    opted_address = AddressTable.objects.get(id=add_id)
    cart = UserCart.objects.filter(user=opted_address.user.user_id)
    if request.session.has_key('coupon_off'):
        coupon_off = request.session['coupon_off']
    else:
        coupon_off = 0
    for i in cart:
        if i.product.category_name.discount == 0:
            total_price = (i.count*i.product.price) - coupon_off
            Order.objects.create(user=i.user,product=i.product,address=opted_address,status='ordered',count=i.count,price=total_price,payment_method='paypal')
            i.delete()
            coupon_off = 0
        else:
            total_price = (i.count*float(i.product.discount_price)) - coupon_off
            Order.objects.create(user=i.user,product=i.product,address=opted_address,status='ordered',count=i.count,price=total_price,payment_method='paypal')
            i.delete()
            coupon_off = 0
    if request.session.has_key("coupon_off"):
        del request.session['coupon_off']         
    del request.session['id']
    current_user  = User.objects.get(id=request.user.id)
    current_myuser = MyUsers.objects.get(user=current_user)
    current_myuser.referral_earnings = 0
    current_myuser.save()
    return JsonResponse('true', safe=False)
def payrazor(request):
    try:
        add_id = request.session['id']
    except:
        messages.info(request,'please select an address')
        return redirect(checkout)
    opted_address = AddressTable.objects.get(id=add_id)
    cart = UserCart.objects.filter(user=opted_address.user.user_id)
    if request.session.has_key('coupon_off'):
        coupon_off = request.session['coupon_off']
    else:
        coupon_off = 0
    for i in cart:
        if i.product.category_name.discount == 0: 
            total_price = (i.count*i.product.price) - coupon_off
            Order.objects.create(user=i.user,product=i.product,address=opted_address,status='ordered',count=i.count,price=total_price,payment_method='razorpay')
            i.delete()
            coupon_off = 0
            
        else:
            total_price = (i.count*float(i.product.discount_price)) - coupon_off
            Order.objects.create(user=i.user,product=i.product,address=opted_address,status='ordered',count=i.count,price=total_price,payment_method='razorpay')
            i.delete()
            coupon_off = 0
    if request.session.has_key("coupon_off"):
        del request.session['coupon_off']  
    del request.session['id']
    current_user  = User.objects.get(id=request.user.id)
    current_myuser = MyUsers.objects.get(user=current_user)
    current_myuser.referral_earnings = 0
    current_myuser.save()
    return redirect(successpayment)

def paypalrazor(request,id):
    current_user = User.objects.get(id=request.user.id)
    current_myuser = MyUsers.objects.get(user= current_user) 
    current_address = AddressTable.objects.filter(user=current_myuser)
    current_usercart = UserCart.objects.filter(user=current_myuser)
    category = Categories.objects.all()
    grandtotal = request.session['grandtotal']
    if request.session.has_key('coupon_off'):
        grandtotal = grandtotal-request.session['coupon_off'] 
    if id==1: 
        return render(request, 'payment.html',{'total':grandtotal,'user':current_user})
    elif id==2:
        return render(request,'payrazor.html' ,{'total':grandtotal,'user':current_user})
        
def userprofile(request):
    myuser = MyUsers.objects.get(user= request.user)
    addresses = AddressTable.objects.filter(user=myuser)
    orders = Order.objects.filter(user=myuser)
    usercarts = UserCart.objects.filter(user=myuser)
    context = {'myuser':myuser,'addresses':addresses,'orders':orders,'usercarts':usercarts}
    return render(request,'userprofile2.html', context)
    
def order_cancel(request,id):
    current_order = Order.objects.get(id=id)
    current_order.delete()
    return redirect(userprofile)

def edituser(request,id):
    current_user = User.objects.get(id=id)
    current_myuser = MyUsers.objects.get(user=current_user)
    if request.method == 'POST':
        current_user.first_name = request.POST['first_name']
        current_user.last_name = request.POST['last_name']
        current_user.email = request.POST['email']
        current_myuser.phone_number = request.POST['phone_number']
        current_myuser.image = request.FILES.get('user_image')
        current_user.save()
        current_myuser.save ()
        print(current_myuser.user.last_name)
        return JsonResponse('true',safe=False)  
    else: 
        return render(request, 'userprofileedit.html', {'user':current_myuser}) 

def changepassword(request,id):
    user = User.objects.get(id=id)
    if request.method=='POST':
        password = request.POST['current_password']
        lastpassword = request.user.password
        check_status = check_password(password,lastpassword)
        if check_status != True:
            return JsonResponse('false',safe=False)
        else:
            new_password = request.POST['password1']
            user.set_password(new_password)
            user.save()
            return JsonResponse('true',safe=False)
    else:
         return render(request,'changepassword.html',{'user':user})

def loginwithphone(request):
    if request.method =='POST':
        global phone_number
        phone_number = request.POST['phone']
        if MyUsers.objects.filter(phone_number=phone_number).exists():
            global otp
            otp = random.randint(1000,9999)
            account_sid = 'AC14dc0259b0ab2fc4ca0bc5a34d764fc6'
            auth_token = '51b99540aa3a9c09b9ff5781596d93b1'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                              body=f"This is your OTP {otp}",
                              from_='+13059648490',
                              to= f'+919207697719'
                          )
            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false', safe=False)        
    else:
        return render(request,'otplogin.html')

@csrf_exempt 
def otpconfirmation(request): 
    if request.method =='POST':
        global phone_number
        myuser = MyUsers.objects.get(phone_number=phone_number)
        user = User.objects.get(username=myuser.user.username) 
        OTP = request.POST['otp']
        OTP = int(OTP)
        global otp
        if otp == OTP:
            auth.login(request,user)
            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)
    else:
        return render(request, 'otpconfirmation.html')

def successpayment(request):
    return render(request,'successpage.html')

def product_search(request):
    name = request.GET['search_input']
    searched_products = ProductDetails.objects.filter(name__icontains = name) or ProductDetails.objects.filter(discription__icontains = name)
    category = Categories.objects.all()
    context = {'products':searched_products ,'category':category}
    return render(request,'search_products.html',context)

def search_show(request):
    searched_products = request.session['search_product']
    category = Categories.objects.all()
    context = {'products':searched_products ,'category':category}
    return render(request,'search_products.html',context)

def userlogout(request):
    auth.logout(request)
    return redirect(home)

    

    
        

  

    
    



    
          



from django.db import models
from django.contrib.auth.models import User
from admin1.models import Categories,ProductDetails
from django.utils.datetime_safe import datetime


# Create your models here.
  
class MyUsers(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE,null=True,blank=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True)
    image = models.ImageField(upload_to='user_profile/', null=True)
    referral_code = models.CharField(max_length=12,blank=True)
    recommended_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='ref_by')
    referral_earnings = models.IntegerField(blank=True,null=True)


    @property
    def imageuserurl(self):
        if self.image== '':
            image1 = ''
        else:
            image1 = self.image.url
        return image1
    
  
class UserCart(models.Model):
    user = models.ForeignKey(MyUsers ,on_delete= models.CASCADE )
    product = models.ForeignKey(ProductDetails , on_delete= models.CASCADE )
    count = models.PositiveIntegerField(default=1)
    date = models.DateField(auto_now_add=True)

class AddressTable(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    housename = models.CharField(max_length=100)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=20) 
    pincode = models.CharField(max_length=6)
    
class Order(models.Model):
    user = models.ForeignKey(MyUsers,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressTable, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    payment_method = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
class Wishlist(models.Model):
    user = models.ForeignKey(MyUsers ,on_delete= models.CASCADE )
    product = models.ForeignKey(ProductDetails , on_delete= models.CASCADE )
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2,max_digits=10)



   
    

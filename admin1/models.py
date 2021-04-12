from django.db import models
from django.contrib.auth.models import User
import decimal
# Create your models here.
class Categories(models.Model):
    category = models.CharField(max_length=20)
    discount = models.IntegerField(default = 0) 
class ProductDetails(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places =2, max_digits= 10)
    weight = models.DecimalField(decimal_places =2, max_digits= 10)
    discription =models.TextField()
    image1 = models.ImageField(upload_to='media/')
    image2 = models.ImageField(upload_to='media/')
    image3 = models.ImageField(upload_to='media/')
    category_name = models.ForeignKey(Categories, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    @property
    def discount_price(self):
        discounted_price =(self.price) - (self.price * (decimal.Decimal(self.category_name.discount) / 100))
        discounted_price = format( discounted_price, ".2f")
        return discounted_price
    @property
    def imageurl(self):
        if self.image1== '':
            image = ''
        else:
            image = self.image1.url
        return image
     
    @property
    def imageurl2(self):
        if self.image2== '':
            image = ''
        else:
            image = self.image2.url
        return image

    @property
    def imageurl3(self):
        if self.image3== '':
            image = ''
        else:
            image = self.image3.url
        return image
class Coupon(models.Model):
    code = models.CharField(max_length=10,blank = True, null = True)  
    off = models.IntegerField(blank = True,null = True)
    status = models.BooleanField(default=True) 

    
    
from django.db import models
from accounts.models import Profile
from product.models import Product


RELEVANCE_CHOICES = (
    (1,("waiting")),
    (2,("paid")),
    (3,("sent")),
    (4,("delivered")),
    (5,("canceled")),

)

class Order(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status = models.CharField(choices=RELEVANCE_CHOICES,max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class Basket(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
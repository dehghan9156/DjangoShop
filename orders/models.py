from decimal import Decimal

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

class HeaderFactor(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    status = models.CharField(choices=RELEVANCE_CHOICES,max_length=250,default='waiting')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}-{self.profile.first_name}"

class Factor(models.Model):
    headerfactor = models.ForeignKey(HeaderFactor,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        price = self.product.price
        discount_percentage = Decimal(str(self.product.discount)) if self.product.discount else Decimal(0)  # تبدیل تخفیف به Decimal
        discount_amount = (price * discount_percentage) / Decimal(100)
        final_price_per_item = price - discount_amount
        total_price = final_price_per_item * self.quantity
        return total_price

    def __str__(self):
        return f"{self.pk}-{self.product.name}"

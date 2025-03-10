from django.db import models

class Product(models.Model):
    category = models.ForeignKey("Category",on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)  # تخفیف درصدی (مثلاً ۱۰٪)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(blank=True,null=True)

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"
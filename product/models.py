from django.db import models

class Product(models.Model):
    category = models.ForeignKey("Category",on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    discount = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/',blank=True,null=True)  # فیلد تصویر
    external_image_url = models.URLField(blank=True, null=True)

    def image_display_url(self):
        if self.image:
            return self.image.url
        elif self.external_image_url:
            return self.external_image_url
        return None

    def __str__(self):
        return f"{self.id}--{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"
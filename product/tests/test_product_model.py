from django.urls import reverse, resolve
from unittest import TestCase
from product.models import Category,Product

class  TestModels(TestCase):
    def setUp(self):
        self.category_obj = Category.objects.create(name="test",description="test")

    def test_product_model(self):
        product = Product.objects.create(
            category = self.category_obj,
            name = 'test',
            description = 'test',
            price = 45000,
            discount = 5,
            stock = 5,
            image = 'test'
        )
        self.assertEqual(product.name,'test')
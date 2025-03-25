from django.urls import reverse, resolve
from unittest import TestCase
from product.models import Category
from product.forms import ProductCreateUpdateForm

class TestForms(TestCase):
    def test_product_create_update_form(self):
        category_obj = Category.objects.create(name='test')
        form = ProductCreateUpdateForm(data={
            'category':category_obj,
            'name':'test',
            'description':'test',
            'price':45000,
            'stock':5,
            'image':'test'
        })
        self.assertTrue(form.is_valid())
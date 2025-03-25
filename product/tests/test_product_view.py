from http.client import responses

from django.urls import reverse, resolve
from unittest import TestCase
from product.models import Category,Product
from django.test import Client

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.category_obj = Category.objects.create(name='tets',description='test')
        self.product = Product.objects.create(
            category = self.category_obj,
            name = 'test',
            description = 'test',
            price = 4500,
            discount = 4,
            stock = 5,
            image = 'test'
        )
    def test_product_list_view(self):
        url = reverse('product:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_product_detail_view(self):
        url = reverse('product:product-detail',kwargs={'pk':self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_product_update_view(self):
        url = reverse('product:product-update',kwargs={'pk':self.product.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code,302)

    def test_product_delete_view(self):
        url = reverse('product:product-delete',kwargs={'pk':self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code,302)

    def test_product_create_view(self):
        url = reverse('product:product-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code,200)

    def test_product_category_view(self):
        url = reverse('product:product-category',kwargs={'pk':self.category_obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)


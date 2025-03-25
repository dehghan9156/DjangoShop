from django.urls import reverse, resolve
from unittest import TestCase
from product.views import ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductCreateView, \
    ProductCategoryShowView


class TestUrls(TestCase):
    def test_product_list_url(self):
        url = reverse('product:product-list')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail_url(self):
        url = reverse('product:product-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_product_update_url(self):
        url = reverse('product:product-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProductUpdateView)

    def test_product_delete_url(self):
        url = reverse('product:product-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProductDeleteView)

    def test_product_create(self):
        url = reverse('product:product-create')
        self.assertEqual(resolve(url).func.view_class, ProductCreateView)

    def test_product_category(self):
        url = reverse('product:product-category', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, ProductCategoryShowView)

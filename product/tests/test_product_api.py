from http.client import responses
import pytest
from pytest_django.fixtures import client
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from product.models import Product, Category
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def user_obj():
    user = User.objects.create_user(email='test@test.com', password='testpass')
    return user


@pytest.fixture
def category_obj():
    category = Category.objects.create(
        name="test",
        description="test"
    )
    return category


@pytest.fixture
def product_obj(category_obj):
    product = Product.objects.create(
        category=category_obj,
        name="test",
        description="test",
        price=4000,
        discount=5,
        stock=5)
    return product


@pytest.mark.django_db
class TestProductApi:
    def test_product_list_view(self, api_client):
        url = reverse('product:api-v1:product-list-api')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_product_detail_view(self, api_client, product_obj):
        url = reverse('product:api-v1:product-detail-api', kwargs={'pk': product_obj.pk})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_product_create_201_view(self, api_client, user_obj,category_obj):
        user = user_obj
        api_client.force_authenticate(user=user)
        url = reverse('product:api-v1:product-create-api')
        data = {
            'category' : category_obj.name,
            'name' : "test",
            'description' : "test",
            'price' : 4000,
            'discount' : 5,
            'stock' : 5,
        }
        response = api_client.post(url, data,format="json")
        print(response.status_code, response.data)  # نمایش خطا در صورت بروز مشکل
        assert response.status_code == 201

    def test_product_create_401_view(self, api_client, user_obj,category_obj):
        # user = user_obj
        # api_client.force_authenticate(user=user)
        url = reverse('product:api-v1:product-create-api')
        data = {
            'category' : category_obj.name,
            'name' : "test",
            'description' : "test",
            'price' : 4000,
            'discount' : 5,
            'stock' : 5,
        }
        response = api_client.post(url, data,format="json")
        print(response.status_code, response.data)  # نمایش خطا در صورت بروز مشکل
        assert response.status_code == 401

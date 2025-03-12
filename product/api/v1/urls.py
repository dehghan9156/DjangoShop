"""
URL configuration for DjangoShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from accounts.api.v1.urls import app_name
from . import views

app_name = 'api-v1'

urlpatterns = [
    path("",views.ProductListApiView.as_view(),name="product-list-api"),
    path("detail/<int:pk>/",views.ProductDetailApiView.as_view(),name="product-detail-api"),
    path("create/",views.ProductCreateApiView.as_view(),name="product-create-api"),

]
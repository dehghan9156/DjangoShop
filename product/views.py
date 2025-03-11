from django.views.generic import ListView,DetailView,UpdateView
from django.shortcuts import render
from .models import Product,Category

# Create your views here.
class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'product/index.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/update.html'
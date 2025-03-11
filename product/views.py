from django.views.generic import ListView,DetailView,UpdateView
from django.shortcuts import render,redirect
from rest_framework.reverse import reverse_lazy

from .models import Product,Category
from .forms import ProductUpdateForm
from django.contrib import messages



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
    form_class = ProductUpdateForm

    def get_success_url(self):
        return reverse_lazy('product:product-detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'You cannot edit product', 'error')
            return redirect("product:product-list")
        else:
            messages.success(request, 'Product successfully updated.', 'success')
        return super().dispatch(request, *args, **kwargs)


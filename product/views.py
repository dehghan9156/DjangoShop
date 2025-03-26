from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from django.shortcuts import render,redirect
from rest_framework.reverse import reverse_lazy
from unicodedata import category
from django.views import View
from .models import Product,Category
from .forms import ProductCreateUpdateForm
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
    form_class = ProductCreateUpdateForm

    def get_success_url(self):
        return reverse_lazy('product:product-detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'You cannot edit product', 'error')
            return redirect("product:product-list")
        # else:
        #     messages.success(request, 'Product successfully updated.', 'success')
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    def get_success_url(self):
        messages.success(self.request,"product delete successfuly",'success')
        # print("Messages in session:", list(messages.get_messages(self.request)))
        return reverse_lazy("product:product-list")

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = 'product/create.html'
    def get_success_url(self):
        messages.success(self.request,"product add successfully.",'success')
        return reverse_lazy("product:product-list")

class ProductCategoryShowView(View):
    def get(self,request,pk):
        category = Category.objects.get(pk=pk)
        products = Product.objects.filter(category=category)
        return render(request,'product/product-category.html',{'products':products})



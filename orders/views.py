from django.contrib.messages import success
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.reverse import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import Basket
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile, User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from collections import Counter
from .forms import EdithBasketForm


class CreateBasketView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        profile = get_object_or_404(Profile, user=self.request.user)
        basket_item = Basket.objects.filter(product=product, profile=profile).first()
        # print(basket_item)
        if basket_item:
            messages.info(request, "this product exist in basket", 'info')
            basket_item.quantity += 1
            basket_item.save()

        else:
            Basket.objects.create(
                profile=profile,
                product=product
            )
            messages.success(request, "Add Product In Your Basket", 'success')
        return redirect("product:product-detail", pk=pk)


class ShowBasketView(LoginRequiredMixin, ListView):
    model = Basket
    template_name = "orders/show.html"
    context_object_name = "baskets"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        baskets = Basket.objects.filter(profile=profile)
        return baskets


    """update counter basket """
    def post(self,request):
        form = EdithBasketForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            basket_id = request.POST.get('basket_id')
            basket = get_object_or_404(Basket, id=basket_id)
            basket.quantity = quantity
            basket.save()
        return redirect("orders:show-basket")

class DeleteProductView(LoginRequiredMixin,View):
    def get(self,request,pk):
        basket = get_object_or_404(Basket,pk=pk)
        basket.delete()
        return redirect('orders:show-basket')

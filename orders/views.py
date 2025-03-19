from django.contrib.messages import success
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.reverse import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import Factor, HeaderFactor
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile, User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from collections import Counter
from .forms import EdithFactorForm
import requests


class CreateFactorView(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = get_object_or_404(Profile, user=self.request.user)
        headerfactor = HeaderFactor.objects.filter(profile=profile).first()
        if not headerfactor:
            headerfactor = HeaderFactor.objects.create(
                profile=profile
            )
        else:
            messages.info(request, "Header factor already exists", 'info')
        factor = Factor.objects.filter(headerfactor=headerfactor,product=pk).first()
        if not factor:
            product = get_object_or_404(Product, pk=pk)
            Factor.objects.create(
                headerfactor=headerfactor,
                product=product,
            )
        else:
            factor.quantity +=1
            factor.save()
        return redirect('product:product-detail', pk=pk)

class ShowFactorView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=self.request.user)
        headerfactor = get_object_or_404(HeaderFactor, profile=profile)
        factors = Factor.objects.filter(headerfactor=headerfactor)
        lst = []
        for factor in factors:
            lst.append(factor.total_price)
        total_factor = sum(lst)
        final_price = total_factor + 52000
        return render(request, "orders/show.html",{
            'factors': factors,'total_factor':total_factor,
            'final_price':final_price,
            'headerfactor_id':headerfactor.pk

        })

class DeleteProductView(LoginRequiredMixin, View):
    def get(self, request, pk):
        factor = get_object_or_404(Factor, pk=pk)
        factor.delete()
        return redirect('orders:show-factor')

class UpdateFactorView(View):
    def post(self,request,pk):
        profile = Profile.objects.get(user=self.request.user)
        product = get_object_or_404(Product,pk=pk)
        headerfactor = get_object_or_404(HeaderFactor,profile=profile)
        factor = Factor.objects.filter(headerfactor=headerfactor,product=product).first()
        new_quantity = request.POST.get('quantity',1)
        if factor:
            factor.quantity = new_quantity
            factor.save()
            messages.info(request, "Product quantity updated", 'info')
        else:
            Factor.objects.create(
                headerfactor=headerfactor,
                product=product,
                quantity = 1
            )
            messages.info(request, "Product added to cart", 'info')
        return redirect('orders:show-factor')

class OrderSummeryView(LoginRequiredMixin,View):
    def get(self,request,pk):
        headerfactor = HeaderFactor.objects.get(pk=pk)
        factors = Factor.objects.filter(headerfactor=headerfactor)
        lst=[]
        for factor in factors:
            lst.append(factor.total_price)
        total_factor = sum(lst)
        final_price = total_factor + 52000
        return render(request,'orders/oreder-summery.html',{
            'headerfactor':headerfactor,
            'factors':factors,
            'total_factor':total_factor,
            'final_price':final_price,
            'headerfactor_id':headerfactor.pk
        })




# مقدار مرچنت کد تستی (Sandbox)
MERCHANT = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
CALLBACK_URL = "http://127.0.0.1:8000/orders/payment/verify/"  # آدرس بازگشت بعد از پرداخت

class ZarinPalPaymentView(View):
    def get(self, request, pk):
        """ارسال درخواست پرداخت به زرین‌پال"""
        try:
            headerfactor = HeaderFactor.objects.get(pk=pk)
            factors = Factor.objects.filter(headerfactor=headerfactor)
            lst = []
            for factor in factors:
                lst.append(factor.total_price)
            total_factor = sum(lst)
            final_price = total_factor + 52000
            amount = int(final_price)  # مبلغ پرداختی

            data = {
                "merchant_id": MERCHANT,
                "amount": amount,
                "callback_url": f"{CALLBACK_URL}{pk}/",
                "description": f"پرداخت فاکتور شماره {headerfactor.pk}",
            }
            headers = {"Content-Type": "application/json"}

            response = requests.post(
                "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
                json=data,
                headers=headers
            )
            result = response.json()

            if "data" in result and "authority" in result["data"]:
                return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{result['data']['authority']}")
            else:
                return render(request, "payment/error.html", {"message": result["errors"]["message"]})

        except HeaderFactor.DoesNotExist:
            return render(request, "payment/error.html", {"message": "فاکتور یافت نشد."})

class ZarinPalVerifyView(View):
    def get(self, request,pk):
        headerfactor = HeaderFactor.objects.get(pk=pk)
        factors = Factor.objects.filter(headerfactor=headerfactor)
        lst = []
        for factor in factors:
            lst.append(factor.total_price)
        total_factor = sum(lst)
        final_price = total_factor + 52000
        amount = int(final_price)  # مبلغ پرداختی

        """بررسی وضعیت پرداخت بعد از بازگشت از درگاه"""
        authority = request.GET.get("Authority")
        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": authority
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post("https://sandbox.zarinpal.com/pg/v4/payment/verify.json", json=data, headers=headers)
        result = response.json()

        if "data" in result and "code" in result["data"]:
            if result["data"]["code"] == 100:
                headerfactor.status = "paid"
                Factor.objects.filter(headerfactor=headerfactor).delete()
                headerfactor.save()
                return render(request, "payment/success.html", {"transId": result["data"]["ref_id"]})
            else:
                return render(request, "payment/error.html", {"message": f"خطای پرداخت: {result['data']} "})
        elif "errors" in result:
            return render(request, "payment/error.html", {"message": f"خطای زرین‌پال: {result['errors']} "})
        else:
            return render(request, "payment/error.html", {"message": "پاسخ نامعتبر از زرین‌پال"})

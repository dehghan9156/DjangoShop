from .models import HeaderFactor, Factor
from accounts.models import Profile, User
from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product,Category

def cart_count(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        headerfactor = get_object_or_404(HeaderFactor, profile=profile)
        factor = Factor.objects.filter(headerfactor=headerfactor)
        cart_count = factor.count()
    else:
        cart_count = 0

    return {'cart_count':cart_count}


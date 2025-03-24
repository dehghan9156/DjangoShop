from http.client import responses
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.generics import CreateAPIView,ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from accounts.models import Profile
from orders.models import HeaderFactor,Factor
from product.models import Product,Category
from .serialization import HeaderFactorSerializer,FactorSerializer




class ShowFactorApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FactorSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        factor = Factor.objects.filter(headerfactor__id = pk)
        return factor

class UpdateFactorApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        profile = get_object_or_404(Profile,user=self.request.user)
        product = get_object_or_404(Product,pk=pk)
        headerfactor = HeaderFactor.objects.get(profile=profile)
        factor = Factor.objects.filter(headerfactor=headerfactor,product=product).first()
        new_quantity = request.data.get('quantity',1)
        print(f"New quantity received: {new_quantity}")
        if factor:
            factor.quantity = new_quantity + 1
            factor.save()
            return Response({"message": "Product quantity updated"}, status=status.HTTP_200_OK)
        else:
            Factor.objects.create(
                headerfactor=headerfactor,
                product=product,
                quantity=1
            )
            return Response( {"message": "Product added to cart"}, status=status.HTTP_201_CREATED)

class DeleteFactorView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk):
        profile = Profile.objects.get(user=self.request.user)
        product = Product.objects.get(pk=pk)
        headerfactor = HeaderFactor.objects.get(profile=profile)
        factor = Factor.objects.filter(headerfactor=headerfactor,product=product).first()

        if factor:
            factor.delete()
            return Response({'message':'factor delete successfully.'},status=status.HTTP_200_OK)
        else:
            return Response({'error':'factor does not exit.'},status=status.HTTP_404_NOT_FOUND)


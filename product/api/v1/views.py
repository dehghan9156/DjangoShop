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
from .serialization import ProductObjectsSerializer
from ...models import Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class ProductListApiView(generics.ListAPIView):
    serializer_class = ProductObjectsSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['id','name','stock','price']
    search_fields  = ['id','name','stock']
    ordering_fields = ['id','name','stock']

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductObjectsSerializer
    permission_classes = [IsAdminUser]
    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.get("pk"))
        return obj

class ProductCreateApiView(generics.CreateAPIView):
    serializer_class = ProductObjectsSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

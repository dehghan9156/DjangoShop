from http.client import responses

from django.conf import settings
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django.template.defaulttags import querystring
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView
from accounts.models import User
from .serialization import RegisterSerializer


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data ={"email":email}
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

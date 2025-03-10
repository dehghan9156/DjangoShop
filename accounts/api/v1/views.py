from http.client import responses
from django.conf import settings
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView
from accounts.models import User,Profile
from .serialization import (RegisterSerializer,TokenCustomObtainPairSerializer,
                            ChangePasswordSerializer,DisplayProfileUserSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView

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

class TokenCustomObtainPairView(TokenObtainPairView):
    serializer_class = TokenCustomObtainPairSerializer

class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisplayProfileUserView(generics.RetrieveUpdateAPIView):
    serializer_class = DisplayProfileUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.queryset
        profile = get_object_or_404(queryset,user=self.request.user)
        return profile
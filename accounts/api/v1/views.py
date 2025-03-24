from http.client import responses

import jwt
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
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, Profile
from .serialization import (RegisterSerializer, TokenCustomObtainPairSerializer,
                            ChangePasswordSerializer, DisplayProfileUserSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import send_mail

class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            send_mail(
                template_name="email/active_user.tpl",
                context={"token": token},
                from_email="admin@admin.com",
                recipient_list=[email],
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


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
        profile = get_object_or_404(queryset, user=self.request.user)
        return profile

class ConfirmTokenView(APIView):
    def get(self, request, token, *args, **kwargs):
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = token.get("user_id")
        user = get_object_or_404(User,pk=user_id)
        if user.is_verified:
            return Response({'messages':'user already verified.'})
        user.is_verified=True
        user.save()
        return Response(token)
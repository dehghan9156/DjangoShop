from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import RegisterApiView,TokenCustomObtainPairView
from django.views.generic import TemplateView

app_name = 'api-v1'

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('jwt/create/', TokenCustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/',views.ChangePasswordView.as_view(),name='change-password'),
    path('profiel/',views.DisplayProfileUserView.as_view(),name='profile'),
    path("confirm-user/<str:token>/",views.ConfirmTokenView.as_view(),name='confirm-token'),
]
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import RegisterApiView
from django.views.generic import TemplateView

app_name = 'api-v1'

urlpatterns = [
    path('register/',views.RegisterApiView.as_view(),name='register'),
]
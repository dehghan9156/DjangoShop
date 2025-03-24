from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index-accounts'),
    path('login/',views.UserLoginView.as_view(),name='user-login'),
    path('logout/',views.UserLogoutView.as_view(),name='user-logout'),

    path('register/',views.UserRegisterView.as_view(),name='user-register'),
    path('edit/profile/',views.EditProfileView.as_view(),name='edit-profile'),
    path('api/v1/',include('accounts.api.v1.urls'))
]
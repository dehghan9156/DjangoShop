from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from .forms import LoginUserForm,RegisterUserForm,EditProfileForm
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()
class IndexView(View):
    def get(self,request):
        return HttpResponse("yes")

class UserLoginView(View):
    def get(self,request):
        form = LoginUserForm()
        return render(request,'accounts/user_login.html',{'form':form})

    def post(self,request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['email'],password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'User Login Successfully', 'success')
                return redirect('product:product-list')
            else:
                messages.error(request, 'User not found', 'error')
        else:
            messages.error(request, 'Invalid form submission', 'error')

        return render(request, 'accounts/user_login.html', {'form': form})

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request, 'User Logout Successfully', 'success')
        return redirect('product:product-list')

class UserRegisterView(View):
    form_class = RegisterUserForm
    template_name = "accounts/user_register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/user_register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['email'], cd['password'])
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            # ایجاد لینک تایید حساب کاربری
            confirmation_link = f"http://127.0.0.1:8000/accounts/confirm-user/{user.id}/"

            # ایجاد محتوای ایمیل از قالب HTML
            subject = "Confirm Your Account"
            message = render_to_string('email/activation_email.html', {
                'user': user,
                'confirmation_link': confirmation_link,
            })

            email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # ارسال از آدرس ایمیل تنظیم‌شده
                [cd['email']],  # ایمیل کاربر
            )
            email.content_subtype = "html"  # تنظیم محتوای ایمیل به HTML

            # ارسال ایمیل
            email.send()
            messages.success(request, 'User Register Successfully', 'success')
            return redirect('accounts:user-login')
        else:
            messages.error(request, 'User not found', 'error')
            return render(request, 'accounts/user_register.html', {'form': form})


class EditProfileView(View):

    def get(self,request):
        profile = Profile.objects.get(user=self.request.user)
        form = EditProfileForm(instance=profile)
        return render(request,'accounts/profile.html',{'form':form,'profile':profile})

    def post(self,request):
        profile = Profile.objects.get(user=self.request.user)
        form = EditProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"profile edit successfully.",'success')
            return render(request,'accounts/profile.html',{'form':form,'profile':profile})
        else:
            messages.error(request,"information not valid.",'error')
            return render(request,'accounts/profile.html',{'form':form,'profile':profile})


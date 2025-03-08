from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from .forms import LoginUserForm,RegisterUserForm
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model



User = get_user_model()
class IndexView(View):
    def get(self,request):
        return HttpResponse("yes")

class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/user_login.html'
    # redirect_authenticated_user = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_default_redirect_url(self):
        return reverse_lazy('accounts:index-accounts')

class UserLogoutView(LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """
    http_method_names = ["post", "options"]
    template_name = "accounts/user_logout.html"
    extra_context = None

    def get_next_page(self):
        return reverse_lazy('accounts:login-user')

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
            messages.success(request, 'User Register Successfully', 'success')
            return redirect('accounts:index-accounts')
        else:
            messages.error(request, 'User not found', 'error')
            return render(request, 'accounts/user_register.html', {'form': form})


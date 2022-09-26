from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.generic import CreateView, FormView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.utils.http import url_has_allowed_host_and_scheme
# import requests

from account.forms import LoginForm, RegisterForm

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration.html'
    success_url ='/'

def homepage(request):
    return render(request, '')

def logout_request(request):
	logout(request)
	return redirect("/")
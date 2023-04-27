from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView

from patient.forms import RegisterForm, LoginForm
from patient.models import Patient


class RegisterView(generic.CreateView):
    template_name = "register.html"
    context_object_name = "form"
    model = Patient
    form_class = RegisterForm
    success_url = "/patient/login/"

class LoginView(generic.FormView):
    template_name = "login.html"
    context_object_name = "form"
    success_url = "/"
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return super(LoginView, self).post(request, *args, **kwargs)
        return super(LoginView, self).post(request, *args, **kwargs)

class LogoutView(LogoutView):
    next_page = "/patient/login/"
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from instagram.forms import RegisterForm


class HomeView(TemplateView):
    template_name = "general/home.html"


class LegalView(TemplateView):
    template_name = "general/legal.html"


class LoginView(TemplateView):
    template_name = "general/login.html"


class RegisterView(CreateView):
    model = User
    template_name = "general/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Se ha registrado correctamente"
        )
        return super().form_valid(form)


class ContactView(TemplateView):
    template_name = "general/contact.html"

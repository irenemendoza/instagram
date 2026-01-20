from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)

from instagram.forms import LoginForm, RegisterForm
from profiles.models import UserProfile


class HomeView(TemplateView):
    template_name = "general/home.html"


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = "profile"


class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    fields = ["profile_picture", "bio", "birth_date"]

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Se ha actualizado tu perfil"
        )
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("profile_detail", args=[self.object.pk])


class LegalView(TemplateView):
    template_name = "general/legal.html"


class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Bienvenido de nuevo, {user.first_name}",
            )
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(
                self.request, messages.ERROR, "Usuario y/o contraseña incorrectos"
            )
            return super(LoginView, self).form_invalid(form)


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


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha desconectado correctamente")
    return HttpResponseRedirect(reverse("login"))

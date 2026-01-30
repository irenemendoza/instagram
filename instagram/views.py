from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from instagram.forms import LoginForm, ProfileFollow, ProfileUpdateForm, RegisterForm
from posts.models import Post
from profiles.models import Follow, UserProfile


class HomeView(TemplateView):
    template_name = "general/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            following = Follow.objects.filter(
                follower=self.request.user.profile
            ).values_list("following__user", flat=True)
            last_posts = Post.objects.filter(user__profile__user__in=following)
        else:
            last_posts = Post.objects.all().order_by("created_at")[:5]
        context["last_posts"] = last_posts
        return context


class ProfileListView(ListView):
    model = UserProfile
    template_name = "general/profile_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserProfile.objects.all().exclude(user=self.request.user)
        return UserProfile.objects.all()


@method_decorator(login_required, name="dispatch")
class ProfileDetailView(DetailView, FormView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = "profile"
    form_class = ProfileFollow

    def get_initial(self):
        self.initial["profile_pk"] = self.get_object().pk
        return super().get_initial()

    def form_valid(self, form):
        profile_pk = form.cleaned_data.get("profile_pk")
        following = UserProfile.objects.get(pk=profile_pk)

        if Follow.objects.filter(
            follower=self.request.user.profile, following=following
        ).exists():
            Follow.objects.filter(
                follower=self.request.user.profile, following=following
            ).delete()
            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Se ha dejado de seguir al usuario: {following.user.username}",
            )

        else:
            Follow.objects.get_or_create(
                follower=self.request.user.profile, following=following
            )
            messages.add_message(
                self.request, messages.SUCCESS, "Usuario seguido correctamente"
            )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("profile_detail", args=[self.get_object().pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Comprobamos si seguimos al usuario
        following = Follow.objects.filter(
            follower=self.request.user.profile, following=self.get_object()
        ).exists()
        context["following"] = following
        return context


@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    form_class = ProfileUpdateForm

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

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


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha desconectado correctamente")
    return HttpResponseRedirect(reverse("login"))

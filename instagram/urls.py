from django.contrib import admin
from django.urls import path

from instagram.views import ContactView, HomeView, LegalView, LoginView, RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("legal/", LegalView.as_view(), name="legal"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("contact/", ContactView.as_view(), name="contact"),
]

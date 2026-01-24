from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from instagram.views import (
    ContactView,
    HomeView,
    LegalView,
    LoginView,
    ProfileDetailView,
    ProfileListView,
    ProfileUpdateView,
    RegisterView,
    logout_view,
)
from posts.views import PostCreateView, PostDetailView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", HomeView.as_view(), name="home"),
        path("legal/", LegalView.as_view(), name="legal"),
        path("login/", LoginView.as_view(), name="login"),
        path("logout/", logout_view, name="logout"),
        path("register/", RegisterView.as_view(), name="register"),
        path("contact/", ContactView.as_view(), name="contact"),
        path("profiles/", ProfileListView.as_view(), name="profiles_list"),
        path("profile/<pk>/", ProfileDetailView.as_view(), name="profile_detail"),
        path(
            "profile/update/<pk>/", ProfileUpdateView.as_view(), name="profile_update"
        ),
        path("post/create/", PostCreateView.as_view(), name="post_create"),
        path("post/<pk>/", PostDetailView.as_view(), name="post_detail"),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from posts.forms import PostCreateForm
from posts.models import Post


@method_decorator(login_required, name="dispatch")
class PostCreateView(CreateView):
    model = Post
    template_name = "posts/post_create.html"
    form_class = PostCreateForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(
            self.request, messages.SUCCESS, "Se ha publicado con éxito"
        )
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

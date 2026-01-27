from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from posts.forms import CommentCreateForm, PostCreateForm
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
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(DetailView, CreateView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object()
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Se ha publicado con éxito"
        )
        return reverse("post_detail", args=[self.get_object().pk])


@login_required
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        messages.add_message(request, messages.INFO, "Se ha quitado Me gusta")
        post.likes.remove(request.user)
    else:
        messages.add_message(request, messages.INFO, "Se ha añadido Me gusta")
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post_detail", args=[pk]))


@login_required
def post_like_ajax(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        request.user.profile.unlike_post(post)
        return JsonResponse(
            {
                "message": "Ya no me gusta esta publicación.",
                "liked": False,
                "nLikes": post.likes.all().count(),
            }
        )
    else:
        request.user.profile.like_post(post)
        return JsonResponse(
            {
                "message": "Me gusta esta publicación.",
                "liked": True,
                "nLikes": post.likes.all().count(),
            }
        )

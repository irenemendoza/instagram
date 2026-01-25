from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from posts.forms import LikeForm, PostCreateForm
from posts.models import Post


@method_decorator(login_required, name="dispatch")
class PostCreateView(CreateView, LikeForm):
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


@method_decorator(login_required, name="dispatch")
class PostDetailView(DetailView, LikeForm):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    form_class = LikeForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["post_pk"] = self.get_object().pk
        return initial

    def form_valid(self, form):
        post_pk = form.cleaned_data.get("post_pk")
        post = Post.objects.get(pk=post_pk)

        post.like.add(self.request.user)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Se ha añadido Me Gusta",
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post_detail", args=[self.get_object().pk])


"""
@method_decorator(login_required, name="dispatch")
class PostLikeView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            messages.success(request, "Like eliminado")
        else:
            post.likes.add(request.user)
            messages.success(request, "Like añadido exitosamente")

        return redirect('home')
        """


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
        post.likes.remove(request.user)
        return JsonResponse(
            {
                "message": "Ya no me gusta esta publicación.",
                "liked": False,
                "nLikes": post.likes.all().count(),
            }
        )
    else:
        post.likes.add(request.user)
        return JsonResponse(
            {
                "message": "Me gusta esta publicación.",
                "liked": True,
                "nLikes": post.likes.all().count(),
            }
        )

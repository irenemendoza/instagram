from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Usuario", on_delete=models.CASCADE, related_name="posts"
    )
    image = models.ImageField("Publlicación", upload_to="posts_images/")
    caption = models.TextField("Texto", max_length=500, blank=True)
    created_at = models.DateField("Publicada en", auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        verbose_name="Me gusta",
        related_name="liked_posts",
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name="Post sobre el que se hace el comentario",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Autor del comentario",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField("Texto del comentario", max_length=300)
    created_at = models.DateTimeField("Creación del comentario", auto_now_add=True)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

from django import forms

from posts.models import Comment, Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["image", "caption"]


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]

from django import forms

from posts.models import Post


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["image", "caption"]


class LikeForm(forms.Form):
    post_pk = forms.IntegerField(widget=forms.HiddenInput())

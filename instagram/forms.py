from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "username", "password", "email"]

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user

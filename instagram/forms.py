import datetime

from django import forms
from django.contrib.auth.models import User

from profiles.models import UserProfile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "bio", "birth_date"]
        widgets = {
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": datetime.date.today().isoformat(),
                }
            ),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label="password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "username", "password", "email"]

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()

        from profiles.models import UserProfile

        UserProfile.objects.create(user=user)

        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput())


class ProfileFollow(forms.Form):
    profile_pk = forms.IntegerField(widget=forms.HiddenInput())

from django import forms
from django.contrib.auth.hashers import check_password
from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from django.conf import settings


class SignupForm(SignupForm):
    nickname = forms.CharField(label="닉네임")

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.nickname = self.cleaned_data["nickname"]
        user.save()
        return user


class LoginForm(LoginForm):
    def login(self, *args, **kwargs):
        remember = forms.BooleanField(required=False)
        if remember:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        return super(LoginForm, self).login(*args, **kwargs)


class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error("password", "비밀번호가 일치하지 않습니다.")

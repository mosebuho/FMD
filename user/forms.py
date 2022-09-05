from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("userid", "name", "email")
        field_classes = {"username": UsernameField}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["image", "userid", "name", "email"]

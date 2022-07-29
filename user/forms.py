from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','name')
        field_classes = {"username": UsernameField}
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

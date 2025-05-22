from django.contrib.auth.forms import UserCreationForm

from house_core.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

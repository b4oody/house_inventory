from django import forms
from django.contrib.auth.forms import UserCreationForm

from house_core.models import User, Room, Apartment


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateRoomForm(forms.ModelForm):
    apartment = forms.ModelChoiceField(queryset=Apartment.objects.all())

    class Meta:
        model = Room
        fields = [
            "room_name",
            "room_description",
            "apartment",
            "area_m2",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        user_apartments = Apartment.objects.filter(user=self.user)
        self.fields["apartment"].queryset = user_apartments

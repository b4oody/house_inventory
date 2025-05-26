from django import forms
from django.contrib.auth.forms import UserCreationForm

from house_core.models import User, Room, Apartment, Item


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateUpdateRoomForm(forms.ModelForm):
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


class CreateItemForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all())

    class Meta:
        model = Item
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        user_rooms = Room.objects.filter(apartment__user=self.user)
        self.fields["room"].queryset = user_rooms


class ItemFilterForm(forms.Form):
    apartment = forms.ChoiceField(choices=[], required=False)
    room = forms.ChoiceField(choices=[], required=False)
    query = forms.CharField(
        required=False,
        label="Пошук",
        widget=forms.TextInput(
            attrs={"placeholder": "Пошук за назвою або брендом"}
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["apartment"].choices = [("all", "Всі квартири")] + [
                (str(apartment.id), apartment.apartment_name)
                for apartment in Apartment.objects.filter(user=self.user)
            ]

            self.fields["room"].choices = [("all", "Всі кімнати")] + [
                (room.id, room.room_name)
                for room in Room.objects.filter(apartment__user=self.user)
            ]


from django import forms
from django.contrib.auth.forms import UserCreationForm

from house_core.models import User, Room, Apartment, Item, Category, Tag


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
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.none(), required=False)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.none(), required=False)

    class Meta:
        model = Item
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        user_rooms = Room.objects.filter(apartment__user=self.user)
        self.fields["room"].queryset = user_rooms

        tags_item = Tag.objects.filter(user=self.user)
        self.fields["tags"].queryset = tags_item

        categories_item = Category.objects.filter(user=self.user)
        self.fields["categories"].queryset = categories_item


class ItemFilterForm(forms.Form):
    apartment = forms.ChoiceField(choices=[], required=False)
    room = forms.ChoiceField(choices=[], required=False)
    query = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={"placeholder": "Search"}
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


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

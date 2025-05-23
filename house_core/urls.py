from django.urls import path, include

from house_core.views import (
    index_page_view,
    ProfilePageView,
    items_page_view,
    apartments_page_view,
    apartment_page_view,
    ApartmentUpdateView,
    ApartmentDeleteView,
    UserRegistrationView,
    ApartmentCreateView,
    room_page_view,
    RoomUpdateView,
    RoomDeleteView,

)

urlpatterns = [

    path("", include("django.contrib.auth.urls")),
    path("registration/", UserRegistrationView.as_view(), name="registration"),

    path("home/profile/<int:pk>/", ProfilePageView.as_view(), name="profile_view"),
    path("", index_page_view, name="index_view"),

    path("home/items/", items_page_view, name="items_view"),

    path("home/apartments/", apartments_page_view, name="apartments_view"),
    path("home/create-aparment/", ApartmentCreateView.as_view(), name="create_apartment"),
    path("home/apartment/<int:pk>/", apartment_page_view, name="pk_apartment_view"),

    path(
        "home/update-apartment/<int:pk>/",
        ApartmentUpdateView.as_view(),
        name="pk_apartment_edit_view"
    ),
    path(
        "home/delete-apartment/<int:pk>/",
        ApartmentDeleteView.as_view(),
        name="pk_apartment_delete_view"
    ),

    path("home/room/<int:pk>/", room_page_view, name="pk_room_view"),
    path(
        "home/update-room/<int:pk>/",
        RoomUpdateView.as_view(),
        name="pk_room_edit_view"
    ),
    path(
        "home/delete-room/<int:pk>/",
        RoomDeleteView.as_view(),
        name="pk_room_delete_view"
    ),

]

app_name = "house_core"

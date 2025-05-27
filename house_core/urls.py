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
    all_rooms_page_view,
    RoomUpdateView,
    RoomDeleteView,
    RoomCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ItemCreateView,
    report_page_view,
    CreateTagView,
    CreateCategoryView,
    ChangePasswordView
)
from house_core.export_backup import export_to_excel

urlpatterns = [

    path("", include("django.contrib.auth.urls")),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change_password"),

    path("home/profile/<int:pk>/", ProfilePageView.as_view(), name="profile_view"),
    path("home/reports/", report_page_view, name="reports_view"),

    path("", index_page_view, name="index_view"),

    path("home/items/", items_page_view, name="items_view"),
    path("home/create-item/", ItemCreateView.as_view(), name="pk_item_create_view"),
    path("home/create-tag/", CreateTagView.as_view(), name="create_tag_view"),
    path("home/create-category/", CreateCategoryView.as_view(), name="create_category_view"),
    path("home/update-item/<int:pk>/", ItemUpdateView.as_view(), name="pk_item_update_view"),
    path("home/delete-item/<int:pk>/", ItemDeleteView.as_view(), name="pk_item_delete_view"),



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

    path("home/rooms/", all_rooms_page_view, name="rooms_view"),
    path("home/room/<int:pk>/", room_page_view, name="pk_room_view"),
    path(
        "home/create-room/",
        RoomCreateView.as_view(),
        name="create_room"
    ),
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

    path("home/reports/export/", export_to_excel, name="export"),
]

app_name = "house_core"

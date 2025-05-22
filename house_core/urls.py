from django.urls import path, include

from house_core.views import (
    index_page_view,
    items_page_view,
    apartments_page_view,
    apartment_page_view,
    ApartmentUpdateView,
    ApartmentDeleteView,

)

urlpatterns = [

    path("", include("django.contrib.auth.urls")),

    path("", index_page_view, name="index_view"),
    path("home/items/", items_page_view, name="items_view"),

    path("home/apartments/", apartments_page_view, name="apartments_view"),
    path("home/apartment/<int:pk>/", apartment_page_view, name="pk_apartment_view"),
    path("home/apartment/edit/<int:pk>/", ApartmentUpdateView.as_view(), name="pk_apartment_edit_view"),
    path("home/apartment/delete/<int:pk>/", ApartmentDeleteView.as_view(), name="pk_apartment_delete_view"),

]

app_name = "house_core"

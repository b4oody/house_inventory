from django.urls import path

from house_core.views import (
    index_page_view,
    items_page_view,
    apartments_page_view,

)

urlpatterns = [
    path("", index_page_view, name="index_view"),
    path("home/items/", items_page_view, name="items_view"),
    path("home/apartments/", apartments_page_view, name="apartments_view"),
]

app_name = "house_core"

from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"apartments", views.ApartmentViewSet)
router.register(r"rooms", views.RoomViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"items", views.ItemViewSet)
router.register(r"tags", views.TagViewSet)

urlpatterns = [
    path("", include(router.urls)),

]

app_name = "api"

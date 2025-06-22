from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from api import views
from api.views import CreateUserView, CreateTokenView, ManageUserView

router = routers.DefaultRouter()
router.register(r"apartments", views.ApartmentViewSet)
router.register(r"rooms", views.RoomViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"items", views.ItemViewSet)
router.register(r"tags", views.TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", CreateUserView.as_view(), name="create_account"),
    path("login/", CreateTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),

]

app_name = "api"

from rest_framework import viewsets, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from api.serializers import (
    ApartmentSerializer,
    RoomSerializer,
    CategorySerializer,
    ItemSerializer,
    TagSerializer,
    RoomRetrieveSerializer,
    RetrieveItemSerializer,
    UserSerializer
)
from house_core.models import Apartment, Room, Category, Item, Tag


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = (permissions.AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Apartment.objects.filter(user=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return (Room.objects.select_related("apartment")
                .filter(apartment__user=self.request.user)
                )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RoomRetrieveSerializer
        return RoomSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return (Item.objects
                .select_related("room__apartment")
                .prefetch_related("categories", "tags")
                .filter(room__apartment__user=self.request.user)
                )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveItemSerializer
        return ItemSerializer

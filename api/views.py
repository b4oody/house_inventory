from rest_framework import viewsets

from api.serializers import ApartmentSerializer, RoomSerializer, CategorySerializer
from house_core.models import Apartment, Room, Category


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
        return Room.objects.filter(apartment__user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

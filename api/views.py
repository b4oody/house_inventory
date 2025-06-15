from rest_framework import viewsets

from api.serializers import ApartmentSerializer, RoomSerializer
from house_core.models import Apartment, Room


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

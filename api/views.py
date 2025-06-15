from rest_framework import viewsets

from api.serializers import ApartmentSerializer
from house_core.models import Apartment


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Apartment.objects.filter(user=self.request.user)

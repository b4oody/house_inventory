from rest_framework import serializers

from house_core.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "id",
            "apartment_name",
            "address",
            "apartment_description",
            "purchase_price",
            "created_at",
        ]

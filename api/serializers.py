from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from house_core.models import Apartment, Room


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


class RoomSerializer(serializers.ModelSerializer):
    apartment = serializers.CharField()

    class Meta:
        model = Room
        fields = [
            "id",
            "room_name",
            "room_description",
            "apartment",
            "area_m2",
            "created_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        apartment_name = validated_data.pop("apartment", None)
        apartment = get_object_or_404(
            Apartment,
            apartment_name=apartment_name,
            user=self.context["request"].user
        )

        room = Room.objects.create(apartment=apartment, **validated_data)
        return room

    @transaction.atomic
    def update(self, instance, validated_data):
        apartment_name = validated_data.pop("apartment", None)
        if apartment_name:
            apartment = get_object_or_404(
                Apartment,
                apartment_name=apartment_name,
                user=self.context["request"].user
            )
            instance.apartment = apartment
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

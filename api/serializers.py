from django.db import transaction
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from house_core.models import Apartment, Room, Category, Item, Tag


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


class RoomRetrieveSerializer(RoomSerializer):
    apartment = ApartmentSerializer()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "tag_name"]


class ItemSerializer(serializers.ModelSerializer):
    room = serializers.CharField()
    categories = serializers.SlugRelatedField(
        slug_field="category_name",
        queryset=Category.objects.all(), many=True
    )

    tags = serializers.SlugRelatedField(
        slug_field="tag_name",
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Item
        fields = [
            "id",
            "item_name",
            "item_description",
            "photo_url",
            "quantity",
            "purchase_price",
            "current_price",
            "purchase_date",
            "warranty_until",
            "room",
            "categories",
            "model",
            "brand",
            "condition",
            "tags",
            "created_at",
        ]

    def validate_item_name(self, value):
        query = Item.objects.filter(item_name__iexact=value)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("The Item is already exist")
        return value

    def validate_categories(self, value):
        existing_categories_count = Category.objects.filter(category_name__in=value).count()
        if existing_categories_count != len(value):
            raise serializers.ValidationError("One or more categories do not exist.")
        return value

    def validate_tags(self, value):
        existing_tags_count = Tag.objects.filter(tag_name__in=value).count()
        if existing_tags_count != len(value):
            raise serializers.ValidationError("One or more tags do not exist.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        room_name = validated_data.pop("room", None)
        list_categories = validated_data.pop("categories", None)
        list_tags = validated_data.pop("tags", None)

        room = get_object_or_404(
            Room,
            room_name=room_name,
            apartment__user=self.context["request"].user
        )
        item = Item.objects.create(room=room, **validated_data)
        item.categories.set(list_categories)
        item.tags.set(list_tags)

        return item

    @transaction.atomic
    def update(self, instance, validated_data):
        categories = validated_data.pop("categories", None)
        tags = validated_data.pop("tags", None)
        room_name = validated_data.pop("room", None)
        if room_name:
            room = get_object_or_404(
                Room,
                room_name=room_name,
                apartment__user=self.context["request"].user
            )
            instance.room = room

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories is not None:
            instance.categories.set(categories)
        if tags is not None:
            instance.tags.set(tags)
        return instance


class RetrieveItemSerializer(ItemSerializer):
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    room = RoomSerializer()

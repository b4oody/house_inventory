import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings


class WarrantyUntil(models.TextChoices):
    NEW = "new"
    USED = "used"
    UNKNOWN = "unknown"


class User(AbstractUser):
    pass


class Apartment(models.Model):
    apartment_name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Apartment Name",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="apartments"
    )
    address = models.CharField(max_length=100, verbose_name="Address",)
    apartment_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Purchase Price ₴",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apartment_name"]
        unique_together = (("user", "apartment_name"),)

    def __str__(self):
        return self.apartment_name


class Room(models.Model):
    room_name = models.CharField(max_length=100, verbose_name="Room Name")
    room_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name="rooms"
    )
    area_m2 = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Area(m²)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["room_name"]
        unique_together = (("apartment", "room_name"),)

    def __str__(self):
        return self.room_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["category_name"]

    def __str__(self):
        return self.category_name


def upload_to_uuid(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    folder = "photos/"

    return os.path.join(folder, filename)


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField(blank=True, null=True)
    photo_url = models.ImageField(
        upload_to=upload_to_uuid,
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_until = models.DateField(blank=True, null=True)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="items"
    )
    categories = models.ManyToManyField(Category, related_name="items")
    model = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    condition = models.CharField(max_length=50, choices=WarrantyUntil.choices)
    tags = models.ManyToManyField(
        "Tag",
        through="ItemTag",
        related_name="items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["item_name"]
        unique_together = (("room", "item_name"),)
        indexes = [
            models.Index(fields=["item_name"]),
            models.Index(fields=["model"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["purchase_date"]),
            models.Index(fields=["warranty_until"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.item_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["tag_name"]

    def __str__(self):
        return self.tag_name


class ItemTag(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        tags_list = [tag.tag_name for tag in self.item.tags.all()]
        return f"{self.item.item_name}: ({', '.join(tags_list)})"

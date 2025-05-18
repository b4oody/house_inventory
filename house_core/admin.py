from django.contrib import admin

from house_core.models import (
    User,
    Apartment,
    Room,
    Category,
    Item,
    Tag,
    ItemTag
)

admin.site.register(User)
admin.site.register(Apartment)
admin.site.register(Room)
admin.site.register(Category)
admin.site.register(ItemTag)


class ItemTagInline(admin.TabularInline):
    model = ItemTag
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemTagInline]
    list_display = ("item_name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("tag_name",)

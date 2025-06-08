from datetime import date, timedelta
import json, random, uuid, os, pprint, textwrap

APP = "inventory"  # ⚠️  replace with your Django app label if different

fixture = []

# ---- 1. User -----------------------------------------------------------
fixture.append({
    "model": f"{APP}.user",
    "pk": 1,
    "fields": {
        "password": "",
        "last_login": None,
        "is_superuser": False,
        "username": "demo",
        "first_name": "",
        "last_name": "",
        "email": "demo@example.com",
        "is_staff": False,
        "is_active": True,
        "date_joined": "2025-06-01T00:00:00Z"
    }
})

# ---- 2. Apartment ------------------------------------------------------
fixture.append({
    "model": f"{APP}.apartment",
    "pk": 1,
    "fields": {
        "apartment_name": "Sunny Apartment",
        "user": 1,
        "address": "Kyiv, Main St. 1",
        "apartment_description": "Sample apartment for demo data.",
        "purchase_price": "250000.00",
        "created_at": "2025-06-02T00:00:00Z"
    }
})

# ---- 3. Rooms ----------------------------------------------------------
room_names = ["Living Room", "Bedroom", "Kitchen", "Bathroom"]
for i, name in enumerate(room_names, start=1):
    fixture.append({
        "model": f"{APP}.room",
        "pk": i,
        "fields": {
            "room_name": name,
            "room_description": f"{name} description",
            "apartment": 1,
            "area_m2": 15 + i * 2,
            "created_at": "2025-06-02T00:00:00Z"
        }
    })

# ---- 4. Categories -----------------------------------------------------
category_names = ["Electronics", "Furniture", "Appliances"]
for i, name in enumerate(category_names, start=1):
    fixture.append({
        "model": f"{APP}.category",
        "pk": i,
        "fields": {
            "category_name": name,
            "user": 1
        }
    })

# ---- 5. Tags -----------------------------------------------------------
tag_names = ["Urgent", "Sale", "Gift"]
for i, name in enumerate(tag_names, start=1):
    fixture.append({
        "model": f"{APP}.tag",
        "pk": i,
        "fields": {
            "tag_name": name,
            "user": 1
        }
    })

# ---- 6. Items & ItemTags ----------------------------------------------
conditions = ["new", "used", "unknown"]
start_date = date(2024, 6, 1)
for i in range(1, 21):  # 20 items
    room_pk = random.randint(1, len(room_names))
    purchase = start_date + timedelta(days=random.randint(0, 365))
    warranty = purchase.replace(year=purchase.year + 1)
    category_pk = random.randint(1, len(category_names))
    tag_pk = random.randint(1, len(tag_names))

    # Item
    fixture.append({
        "model": f"{APP}.item",
        "pk": i,
        "fields": {
            "item_name": f"Item {i}",
            "item_description": f"Demo description for item {i}.",
            "photo_url": "",
            "quantity": random.randint(1, 5),
            "purchase_price": f"{random.uniform(50, 2000):.2f}",
            "current_price": f"{random.uniform(10, 1500):.2f}",
            "purchase_date": purchase.isoformat(),
            "warranty_until": warranty.isoformat(),
            "room": room_pk,
            "model": f"Model-{i}",
            "brand": f"Brand-{i}",
            "condition": random.choice(conditions),
            "categories": [category_pk],  # ManyToMany via implicit field
            "created_at": "2025-06-02T00:00:00Z"
        }
    })

    # ItemTag (through model)
    fixture.append({
        "model": f"{APP}.itemtag",
        "pk": i,
        "fields": {
            "item": i,
            "tag": tag_pk
        }
    })

# ---- Save to file ------------------------------------------------------
file_path = "items_fixture.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(fixture, f, ensure_ascii=False, indent=2)

file_path

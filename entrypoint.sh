#!/bin/sh

# Чекаємо, поки PostgreSQL буде готовий
# Використовуємо змінні з .env файлу
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Застосовуємо міграції
python manage.py migrate

# Завантажуємо фікстури
python manage.py loaddata items_fixture.json

# Запускаємо основну команду
exec "$@"
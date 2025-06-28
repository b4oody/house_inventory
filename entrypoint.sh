#!/bin/sh

# Зупинити виконання скрипта, якщо будь-яка команда зазнає невдачі
set -e

# Чекаємо, поки база даних буде готова
echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Збираємо всі статичні файли в STATIC_ROOT
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Застосовуємо міграції бази даних
echo "Applying database migrations..."
python manage.py migrate

# Завантажуємо початкові дані (фікстури)
echo "Loading fixtures..."
python manage.py loaddata items_fixture.json # або ваші фікстури

# Передаємо управління основній команді (gunicorn),
# яка вказана в docker-compose.yml або Dockerfile
echo "Starting gunicorn..."
exec "$@"
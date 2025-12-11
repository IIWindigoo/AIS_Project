#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL to be ready..."

# Ждем, пока PostgreSQL будет готов принимать подключения
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing migrations"

# Запускаем миграции Alembic
alembic upgrade head

echo "Migrations completed successfully"

# Запускаем команду, переданную в CMD (uvicorn)
exec "$@"

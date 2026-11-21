#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "1. Adding test movie"
docker compose exec -T db psql -U cinema -d cinema \
  -c "INSERT INTO movies (title, release_year) VALUES ('Test Movie', 2025);"

echo "2. Recreating containers"
docker compose down
docker compose up -d --build

echo "3. Waiting for database"
until docker compose exec -T db pg_isready -U cinema -d cinema; do
  sleep 2
done

echo "4. Checking saved data"
docker compose exec -T db psql -U cinema -d cinema \
  -c "SELECT * FROM movies WHERE title = 'Test Movie';"
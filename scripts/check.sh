#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "1. Checking API"
curl --fail --show-error --silent http://localhost:8000/health
echo

echo "2. Adding a movie"
curl --fail --show-error --silent -X POST http://localhost:8000/movies \
  -H "Content-Type: application/json" \
  -d '{"title":"Arrival","release_year":2016}'
echo

echo "3. Getting movies"
curl --fail --show-error --silent http://localhost:8000/movies
echo

echo "4. Checking containers"
docker compose ps

echo "5. Checking volumes"
docker volume ls
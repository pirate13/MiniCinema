#!/bin/bash

cd "$(dirname "$0")/.."

echo "Starting MiniCinema..."

docker compose up --build -d

docker compose ps
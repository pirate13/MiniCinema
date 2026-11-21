# MiniCinema API: practical project №1

Small, independent REST API demo for the course *Administration of Unix-like Operating Systems*. Uses FastAPI, PostgreSQL, Docker Compose, bridge network and a persistent named volume. No ARLEKIN files or dependencies are used.

## Requirements
- Docker Desktop running (with `docker compose`)
- macOS/Linux terminal
- `curl`

## Full multicontainer deployment (advanced level)
```bash
chmod +x scripts/*.sh
./scripts/deploy.sh
./scripts/check.sh
```
Open http://localhost:8000/docs for Swagger UI.

```bash
curl http://localhost:8000/health
curl http://localhost:8000/movies
curl -X POST http://localhost:8000/movies -H 'Content-Type: application/json' -d '{"title":"Arrival","release_year":2016}'
docker compose ps
docker compose logs --tail=30 api
docker network ls
docker volume ls
```

## Intermediate-level demonstration: host application, container database
Stop both containers, then start ONLY database:
```bash
docker compose down
docker compose up -d db
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DATABASE_URL=postgresql://cinema:cinema_dev_password@localhost:5433/cinema uvicorn app.main:app --host 127.0.0.1 --port 8000
```
In another terminal use `curl http://localhost:8000/health`. The API is on the host and communicates with PostgreSQL in Docker through the mapped port 5433. Stop host Uvicorn with Ctrl+C, then `docker compose up -d --build` to return to full container mode.

## Persistent data demonstration
```bash
./scripts/persistence-check.sh
```
The script inserts a unique record, runs `docker compose down` (without `-v`), recreates the containers, and verifies that the record still exists. **Never use `docker compose down -v` if you wish to preserve this demonstration's data.**

## Basic level: single app container
After starting database with `docker compose up -d db`:
```bash
docker build -t minicinema-api .
docker run --rm --name minicinema-single --network minicinema-lab_cinema_net -p 8000:8000 -e DATABASE_URL=postgresql://cinema:cinema_dev_password@db:5432/cinema minicinema-api
```
Docker Compose ordinarily prefixes network names with the project directory. Check `docker network ls` and replace `minicinema-lab_cinema_net` if your project folder has a different name. (Or use a host application, as above.)

## Screenshots to capture for PDF report
1. `docker compose ps` showing two running containers.
2. Browser: `http://localhost:8000/docs`.
3. Terminal: `curl` POST followed by GET output.
4. `docker network ls` and `docker volume ls`.
5. Terminal output of `./scripts/persistence-check.sh` ending in PASS.
6. Intermediate-level host-run terminal showing uvicorn and successful API request.

## Files
- `app/main.py`: REST endpoints and table initialization
- `Dockerfile`: Python application image
- `compose.yaml`: API, PostgreSQL, bridge network, named volume
- `scripts/deploy.sh`: build and deploy all services
- `scripts/check.sh`: health + basic API test
- `scripts/persistence-check.sh`: persistence verification

This is a learning project; demo database credentials are deliberately simple and are not suitable for production use.

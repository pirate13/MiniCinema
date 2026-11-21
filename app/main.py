"""Small educational REST API with persistent PostgreSQL storage."""
import os
from contextlib import asynccontextmanager
from typing import Annotated

import psycopg
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field
from psycopg.rows import dict_row

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cinema:cinema_dev_password@localhost:5433/cinema",
)


def connect():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title TEXT NOT NULL,
                release_year INTEGER NOT NULL CHECK (release_year BETWEEN 1888 AND 2100)
            )
        """)
    yield


app = FastAPI(title="MiniCinema API", version="1.0.0", lifespan=lifespan)


class MovieIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    release_year: int = Field(ge=1888, le=2100)


class Movie(MovieIn):
    id: int


@app.get("/health")
def health():
    with connect() as conn:
        conn.execute("SELECT 1").fetchone()
    return {"status": "ok", "database": "connected"}


@app.get("/movies", response_model=list[Movie])
def list_movies():
    with connect() as conn:
        return conn.execute(
            "SELECT id, title, release_year FROM movies ORDER BY id"
        ).fetchall()


@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: Annotated[int, Path(ge=1)]):
    with connect() as conn:
        movie = conn.execute(
            "SELECT id, title, release_year FROM movies WHERE id = %s", (movie_id,)
        ).fetchone()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def add_movie(movie: MovieIn):
    with connect() as conn:
        result = conn.execute(
            "INSERT INTO movies (title, release_year) VALUES (%s, %s) "
            "RETURNING id, title, release_year",
            (movie.title, movie.release_year),
        ).fetchone()
    return result


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: Annotated[int, Path(ge=1)]):
    with connect() as conn:
        deleted = conn.execute(
            "DELETE FROM movies WHERE id = %s RETURNING id", (movie_id,)
        ).fetchone()
    if deleted is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None

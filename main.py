from fastapi import FastAPI

from pydantic import BaseModel


class Movie(BaseModel):
    name: str
    id: str
    rating: int
    director: str



app = FastAPI()

movies = {
    "dune": Movie(name="Dune", id="dune", rating=9, director="Denis Villeneuve"),
    "avatar": Movie(name="Avatar", id="avatar", rating=8, director="James Cameron"),
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movies/dune")
async def get_dune() -> Movie | None:
    return movies.get("dune")

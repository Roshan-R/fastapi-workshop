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

@app.get("/movies/all")
async def get_all_movies() -> list[Movie]:
    return list(movies.values())

@app.get("/movies/{id}")
async def get_dune(id) -> Movie | dict:
    return movies.get(id, {"error": "Movie not found"})


from fastapi import FastAPI, Depends, Request

from pydantic import BaseModel
from uuid import uuid4
from contextlib import asynccontextmanager


class Movie(BaseModel):
    name: str
    id: str
    rating: int
    director: str

api_token = "Bearer " + str(uuid4())

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Api Token: ", api_token)
    yield


app = FastAPI(lifespan=lifespan)


movies = {
    "dune": Movie(name="Dune", id="dune", rating=9, director="Denis Villeneuve"),
    "avatar": Movie(name="Avatar", id="avatar", rating=8, director="James Cameron"),
}


async def authenticate_user(request: Request) ->  bool:
    if request.headers.get("authorization"):
        print(request.headers.get("authorization"))
        print(api_token)
        if request.headers.get("authorization") == api_token:
            return True
    return False


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/movies/all")
async def get_all_movies() -> list[Movie]:
    return list(movies.values())

@app.post("/movies/addnew")
async def add_new_movie(movie: Movie) -> dict:
    movies.update({movie.id: movie})
    return {"success": True}

@app.get("/movies/{id}")
async def get_dune(id, is_authenticated: bool = Depends(authenticate_user)) -> Movie | dict:
    if not is_authenticated:
        return {"error": "invalid authentication token"}
    return movies.get(id, {"error": "Movie not found"})



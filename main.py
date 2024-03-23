from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from uuid import uuid4
from contextlib import asynccontextmanager



class Movie(BaseModel):
    name: str
    id: str
    rating: int
    director: str

api_token = ""

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    api_token = uuid4()
    print("Api Token", api_token)
    yield


app = FastAPI(lifespan=lifespan)


movies = {
    "dune": Movie(name="Dune", id="dune", rating=9, director="Denis Villeneuve"),
    "avatar": Movie(name="Avatar", id="avatar", rating=8, director="James Cameron"),
}


async def authenticate_user(request: Request) -> bool:
    print(request.headers, api_token)
    return True


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
    return movies.get(id, {"error": "Movie not found"})



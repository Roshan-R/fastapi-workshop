from fastapi import FastAPI

app = FastAPI()

movies = {
        "dune": {"name": "Dune", "id": "dune", "rating": 9, "director": "Denis Villeneuve"},
        "avatar": {"name": "Avatar", "id": "avatar", "rating": 8},
        }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movies/dune")
async def get_dune():
    return movies.get("dune")

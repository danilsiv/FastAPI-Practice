from fastapi import FastAPI
from online_cinema.routers import users, movies

from online_cinema.database import engine
from online_cinema.models import Base


app = FastAPI(
    title="Online Cinema API",
    version="1.0.0"
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(movies.router)

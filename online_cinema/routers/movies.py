from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from online_cinema.models import Film
from online_cinema.schemas import FilmCreate, FilmRead
from online_cinema.database import get_db


router = APIRouter()


@router.get("/movies/")
async def read_movies(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession=Depends(get_db)
):
    query = select(Film).offset(offset).limit(limit)
    result = await db.execute(query)
    films = result.scalars().all()
    return films


@router.get("/movies/{film_id}", response_model=FilmRead)
async def get_film(film_id: int, db: AsyncSession=Depends(get_db)):
    result = await db.execute(select(Film).where(Film.id == film_id))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.post("/movies/", response_model=FilmRead)
async def create_film(film: FilmCreate, db: AsyncSession=Depends(get_db)):
    new_film = Film(**film.dict())
    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)
    return new_film

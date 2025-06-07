from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.database import get_session
from app.models import Track


router = APIRouter(prefix='/stats')


@router.get("/genres")
async def get_genre_stats(db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(
            Track.genre,
            func.count(Track.id).label("count")
        )
        .group_by(Track.genre)
        .order_by(func.count(Track.id).desc())
    )
    stats = result.all()
    
    return {stat.genre: stat.count for stat in stats}

@router.get("/years")
async def get_year_stats(db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(
            Track.year,
            func.count(Track.id).label("count")
        )
        .group_by(Track.year)
        .order_by(Track.year)
    )
    stats = result.all()
    
    return {stat.year: stat.count for stat in stats}
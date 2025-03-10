from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.app.models.models import Artists, Genres, Tracks


async def get_all_songs(session: AsyncSession):
    stmt = select(Tracks)
    result = await session.execute(stmt)
    songs = result.scalars().all()
    return songs

async def get_all_group(session: AsyncSession):
    stmt = select(Artists)
    result: Result = await session.execute(stmt)
    groups = result.scalars().all()
    return groups

async def get_all_genres(session: AsyncSession):
    stmt = select(Genres)
    result = await session.execute(stmt)
    genres = result.scalars().all()
    return genres

async def get_group_by_id(session: AsyncSession, group_id: int):
    stmt = select(Artists).where(Artists.artist_id == group_id)
    result = await session.execute(stmt)
    group = result.scalar_one_or_none()
    return group
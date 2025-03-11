from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.app.models.models import Artists, Genres, Tracks, Awards


async def get_all_group_songs(session: AsyncSession, artist_id: int):
    stmt = select(Tracks).where(Tracks.artist_id == artist_id)
    result = await session.execute(stmt)
    songs = result.scalars().all()
    return songs

async def get_all_songs(session: AsyncSession):
    stmt = select(Tracks)
    result = await session.execute(stmt)
    songs = result.scalars().all()
    return list(songs)

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

async def get_group_by_id(session: AsyncSession, artist_id: int):
    stmt = select(Artists).where(Artists.artist_id == artist_id)
    result = await session.execute(stmt)
    group = result.scalar_one_or_none()
    return group

async def get_all_awards(session: AsyncSession):
    stmt = select(Awards)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_award_by_artist_id(session: AsyncSession, artist_id: int):
    stmt = select(Awards).where(Awards.artist_id == artist_id)
    result = await session.execute(stmt)
    return result.scalars().all()
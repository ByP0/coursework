from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.app.models.models import Artists, Genres, Tracks, Members, Awards
from backend.app.schemas.add_schemas import AddArtist, AddTrack, AddMember, AddAward
from datetime import datetime, time

async def add_artist(session: AsyncSession, data: AddArtist):
    data_for_db = Artists(
        name=data.name,
        country=data.country,
        formation_year=data.formation_year,
        breakup_year=data.breakup_year,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)


async def add_track(session: AsyncSession, data: AddTrack):
    data_for_db = Tracks(
        title=data.title,
        artist_id=data.artist_id,
        release_year=data.release_year,
        duration=data.duration,
        genre_id=data.genre_id,
    )
    
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)

async def add_member(session: AsyncSession, data: AddMember):
    data_for_db = Members(
        artist_id=data.artist_id,
        full_name=data.full_name,
        role=data.role,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)

async def add_award(session: AsyncSession, data: AddAward):
    data_for_db = Awards(
        artist_id=data.artist_id,
        award_name=data.award_name,
        year=data.year,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)

async def add_genre_start(session: AsyncSession, data: str):
    data_for_db = Genres(
        genre_name=data,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.app.models.models import Artists, Genres, Tracks, Members
from backend.app.schemas.add_schemas import AddArtist, AddTrack, AddGenre, AddMember
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

async def add_genre(session: AsyncSession, data: AddGenre):
    data_for_db = Genres(
        genre_name=data.genre_name,
    )
    session.add(data_for_db)
    await session.commit()
    await session.refresh(data_for_db)

async def add_track(session: AsyncSession, data: AddTrack):
    release_year = datetime.strptime(data.release_year, "%Y").date()

    duration_parts = data.duration.split(':')
    duration_time = time(int(duration_parts[0]), int(duration_parts[1]))
    
    data_for_db = Tracks(
        title=data.title,
        artist_id=data.artist_id,
        release_year=release_year,
        duration=duration_time,
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
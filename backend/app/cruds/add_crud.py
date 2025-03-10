from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from backend.app.models.models import Artists, Genres, Tracks
from backend.app.schemas.add_schemas import AddArtist, AddTrack

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

async def add_genre(session: AsyncSession, name: str):
    data_for_db = Genres(
        name=name,
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
    await session.refresh()
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from datetime import datetime, time
from typing import Optional
from models import *
from databasedb import async_session


async def add_artist_async(name: str, country: str):
    async with async_session() as session:
        try:
            data_for_db = Artists(artist_name=name, country=country)
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)
            return data_for_db
        except Exception as e:
            await session.rollback()
            raise e

async def add_group_async(name: str, country: str, formation_year: int, breakup_year: int):
    async with async_session() as session:
        try:
            data_for_db = Groups(group_name=name, country=country, formation_year=formation_year, breakup_year=breakup_year)
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)
            return data_for_db
        except Exception as e:
            await session.rollback()
            raise e

async def add_track_async(song_title: str, artist_name: Optional[str], group_name: Optional[str], release_year: int, duration: str, genre_name: str):
    async with async_session() as session:
        try:
            if group_name is None and artist_name is None:
                raise ValueError("Необходимо указать хотя бы артиста или группу.")
            if group_name is None:
                data_for_db = Tracks(title=song_title, artist_name=artist_name, release_year=release_year, duration=duration, genre_name=genre_name)
            if artist_name is None:
                data_for_db = Tracks(title=song_title, group_name=group_name, release_year=release_year, duration=duration, genre_name=genre_name)
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)
            return data_for_db
        except Exception as e:
            await session.rollback()
            raise e

async def add_genre_async(genre_name: str):
    async with async_session() as session:
        try:
            data_for_db = Genres(genre_name=genre_name)
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)
            return data_for_db
        except Exception as e:
            await session.rollback()
            raise e

async def add_member_async(group_name: str, full_name: str, role: str):
    async with async_session() as session:
        try:
            data_for_db = Members(group_name=group_name, full_name=full_name, role=role)
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)
            return data_for_db
        except Exception as e:
            await session.rollback()
            raise e

async def add_award_async(
    award_name: str,
    year: int,
    artist_name: Optional[str] = None,
    group_name: Optional[str] = None,
):
    async with async_session() as session:
        try:
            if artist_name is not None:
                data_for_db = Awards(award_name=award_name, year=year, artist_name=artist_name)
            elif group_name is not None:
                data_for_db = Awards(award_name=award_name, year=year, group_name=group_name)
            else:
                raise ValueError("Either artist_name or group_name must be provided.")
            
            session.add(data_for_db)
            await session.commit()
            await session.refresh(data_for_db)
            return data_for_db
        except Exception as e:
            await session.rollback()
            raise e
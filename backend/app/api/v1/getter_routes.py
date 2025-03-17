from typing import Annotated, Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.databases.postgresdb import get_session
from backend.app.cruds.getter_crud import get_all_group, get_all_songs, get_all_genres, get_group_by_id, get_all_group_songs, get_all_awards, get_award_by_artist_id
from backend.app.schemas.getter_schemas import GetArtist


router = APIRouter(prefix="/get", tags=["Get"])


@router.get("/all_artists", response_model=list[GetArtist])
async def get_all_music_artists(
    session: AsyncSession = Depends(get_session),
):
    all_artists = await get_all_group(session=session)
    return all_artists


@router.get("/all_songs")
async def get_songs(
    session: AsyncSession = Depends(get_session),
):
    all_songs = await get_all_songs(session=session)
    return all_songs


@router.get("/all_songs_by")
async def get_songs_group(
    artist_id: Annotated[Optional[int], Query(title="ID артиста (группы)")],
    session: AsyncSession = Depends(get_session),
):
    all_songs = await get_all_group_songs(session=session, artist_id=artist_id)
    return all_songs


@router.get("/all_genres")
async def get_genres(
    session: AsyncSession = Depends(get_session),
):
    all_genres = await get_all_genres(session=session)
    return all_genres   


@router.get("/group/{group_id}")
async def get_info_artist(
    artist_id: int,
    session: AsyncSession = Depends(get_session)
):
    group = await get_group_by_id(session=session, artist_id=artist_id)
    return group


@router.get("/awards")
async def get_awards(
    session: AsyncSession = Depends(get_session)
):
    awards = await get_all_awards(session=session)
    return awards


@router.get("/awards_by")
async def get_artist_awards(
    artist_id: Annotated[Optional[int], Query(title="ID артиста (группы)")],
    session: AsyncSession = Depends(get_session),
):
    awards = await get_award_by_artist_id(session=session, artist_id=artist_id)
    return awards
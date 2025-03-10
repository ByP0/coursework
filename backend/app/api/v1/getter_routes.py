from typing import Annotated
from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from backend.app.services.users_services import dependencies
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.databases.postgresdb import get_session
from backend.app.cruds.getter_crud import get_all_group, get_all_songs, get_all_genres, get_group_by_id


router = APIRouter(prefix="/get", tags=["Get"])


@router.get("/all_groups")
async def get_all_music_groups(
    session: AsyncSession = Depends(get_session),
):
    all_group = await get_all_group(session=session)
    return JSONResponse(
        status_code=200,
        content=all_group,
    )

@router.get("/all_songs_group")
async def get_songs(
    session: AsyncSession = Depends(get_session),
):
    all_songs = await get_all_songs(session=session)
    return JSONResponse(
        status_code=200,
        content=all_songs,
    )

@router.get("/all_genres")
async def get_genres(
    session: AsyncSession = Depends(get_session),
):
    all_genres = await get_all_genres(session=session)
    return JSONResponse(
        status_code=200,
        content=all_genres,
    )

@router.get("/group/{group_id}")
async def get_info_artist(
    group_id: int,
    session: AsyncSession = Depends(get_session)
):
    group = await get_group_by_id(session=session, group_id=group_id)
    return JSONResponse(
        status_code=200,
        content=group,
    )
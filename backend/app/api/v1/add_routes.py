from typing import Annotated
from fastapi import APIRouter, Depends, Body
from backend.app.services.users_services import dependencies
from backend.app.schemas.add_schemas import AddArtist, AddTrack, AddMember, AddAward
from backend.app.cruds.add_crud import add_artist, add_track, add_member, add_award
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.databases.postgresdb import get_session


router = APIRouter(prefix="/add", tags=["Add"], dependencies=dependencies)


@router.post("/artist")
async def add_artist_router(
    data: Annotated[AddArtist, Body()],
    session: AsyncSession = Depends(get_session),
):
    await add_artist(session=session, data=data)
    return JSONResponse(
        status_code=200,
        content={
            'status_code': 200,
            'data': "OK"
        }
    )


@router.post("/song")
async def add_song(
    data: AddTrack,
    session: AsyncSession = Depends(get_session),
):
    await add_track(session=session, data=data)
    return JSONResponse(
        status_code=200,
        content={
            'status_code': 200,
            'data': "OK"
        }
    )


@router.post("/members")
async def add_members(
    data: AddMember,
    session: AsyncSession = Depends(get_session),
):
    await add_member(session=session, data=data)
    return JSONResponse(
        status_code=200,
        content={
            'status_code': 200,
            'data': "OK"
        }
    )


@router.post("/awards")
async def add_awards(
    data: AddAward,
    session: AsyncSession = Depends(get_session),
):
    await add_award(session=session, data=data)
    return JSONResponse(
        status_code=200,
        content={
            'status_code': 200,
            'data': "OK"
        }
    )
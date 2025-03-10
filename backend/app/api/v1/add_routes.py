from typing import Annotated
from fastapi import APIRouter, Depends, Body
from backend.app.services.users_services import dependencies, get_user_id_from_token
from backend.app.schemas.add_schemas import AddArtist, AddTrack
from backend.app.cruds.add_crud import add_artist
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.databases.postgresdb import get_session


router = APIRouter(prefix="/add", tags=["Add"], dependencies=dependencies)


@router.post("/artist")
async def add_artist(
    data: Annotated[AddArtist, Body()],
    session: AsyncSession = Depends(get_session),
):
    await add_artist(session=session, data=data)
    return JSONResponse(
        status_code=200,
        content="OK"
    )

@router.post("/song")
async def add_song(
    data = AddTrack,
    session: AsyncSession = Depends(get_session),
):
    await add_song(session=session, data=data)
    return JSONResponse(
        status_code=200,
        content="OK",
    )

from typing import Annotated
from fastapi import APIRouter, Query
from backend.app.services.users_services import dependencies, get_user_id_from_token


router = APIRouter(prefix="/add", tags=["Add"], dependencies=dependencies)


@router.post("/group")
async def add_group(
):
    pass

@router.post("/song")
async def add_song(
):
    pass
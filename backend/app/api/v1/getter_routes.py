from typing import Annotated
from fastapi import APIRouter, Query


router = APIRouter(prefix="/get", tags=["Get"])


@router.get("/all_groups")
async def get_all_music_groups(
):
    pass

@router.get("/all_songs_group")
async def get_songs(
):
    pass
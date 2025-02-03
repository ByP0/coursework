from typing import Annotated
from fastapi import APIRouter, Query


router = APIRouter(prefix="/add", tags=["Add"])


@router.get("/all_groups")
async def get_all_music_groups():
    pass

@router.get("/all_songs_group")
async def get_songs(
):
    pass

@router.patch("/change_song")
async def change_router(
):
    pass

@router.post("add_group")
async def add_group(
):
    pass

@router.post("add_song")
async def add_song(
):
    pass
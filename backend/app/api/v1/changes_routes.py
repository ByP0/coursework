from typing import Annotated
from fastapi import APIRouter, Query


router = APIRouter(prefix="/add", tags=["Add"])


@router.patch("/change_group")
async def change_router(
):
    pass

@router.patch("/change_song")
async def change_router(
):
    pass
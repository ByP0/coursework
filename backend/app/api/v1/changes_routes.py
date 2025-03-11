from typing import Annotated
from fastapi import APIRouter
from backend.app.services.users_services import dependencies

router = APIRouter(prefix="/change", tags=["Change"], dependencies=dependencies)


@router.patch("/group")
async def change_router(
):
    pass


@router.patch("/song")
async def change_router(
):
    pass
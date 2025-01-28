from fastapi import APIRouter, Query, Path
from typing import Annotated
from datetime import date


router = APIRouter(prefix="/travels", tags=["Travels"])


@router.get("/")
async def buy_ticket():
    pass

@router.get("/{route}")
async def get_comments_by_router(
    route: Annotated[str, Path(title="Номер маршрута")]
):
    pass

@router.get("/router")
async def get_routes_by_date(
    date = Annotated[date, Query()]
):
    pass
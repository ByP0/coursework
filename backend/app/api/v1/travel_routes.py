from fastapi import APIRouter, Query
from typing import Annotated
from datetime import date


router = APIRouter(prefix="/travels")


@router.get("/")
async def buy_ticket():
    pass

@router.get("/{router}")
async def get_comments_by_router():
    pass

@router.get("/router")
async def get_routes_by_date(
    date = Annotated[date, Query()]
):
    pass
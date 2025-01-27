from typing import Annotated
from fastapi import APIRouter, Query


router = APIRouter(prefix="/tickets")


@router.post("/buy")
async def buy_ticket():
    pass

@router.get("/info_ticket")
async def get_comments_by_router():
    pass

@router.post("/returns")
async def add_comment():
    pass
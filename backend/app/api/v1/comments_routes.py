from typing import Annotated
from fastapi import APIRouter, Query


router = APIRouter(prefix="/comments")


@router.get("/last_comments")
async def get_last_comments():
    pass

@router.get("/comments_router")
async def get_comments_by_router():
    pass

@router.post("/{router}")
async def add_comment():
    pass
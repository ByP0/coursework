from typing import Annotated
from fastapi import APIRouter, Query


router = APIRouter(prefix="/admin")


@router.get("/all")
async def get_all_travel_routes():
    pass

@router.get("/router")
async def get_one_router(
    flight_number: Annotated[int, Query(..., title="Flight number", example=104)]
):
    pass

@router.post("/change")
async def change_router(

):
    pass
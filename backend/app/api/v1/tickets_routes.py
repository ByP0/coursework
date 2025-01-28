from fastapi import APIRouter


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/buy")
async def buy_ticket():
    pass

@router.get("/info_ticket")
async def get_comments_by_router():
    pass

@router.post("/returns")
async def add_comment():
    pass
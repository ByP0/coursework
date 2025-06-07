from fastapi import APIRouter
from app.api.v1.routers import artists, stats, tracks

router_v1 = APIRouter(prefix='/v1')

router_v1.include_router(artists.router)
router_v1.include_router(stats.router)
router_v1.include_router(tracks.router)
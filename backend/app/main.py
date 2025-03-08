from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.app.api.v1.add_routes import router as add_routes
from backend.app.api.v1.changes_routes import router as changes_routes
from backend.app.api.v1.getter_routes import router as getter_routes
from backend.app.api.v1.users_routes import router as users_routes
from backend.app.databases.postgresdb import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_routes)
app.include_router(add_routes)
app.include_router(changes_routes)
app.include_router(getter_routes)
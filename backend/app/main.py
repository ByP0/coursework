from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.app.api.v1.add_routes import router as add_routes
from backend.app.api.v1.changes_routes import router as changes_routes
from backend.app.api.v1.getter_routes import router as getter_routes
from backend.app.api.v1.users_routes import router as users_routes
from backend.app.databases.postgresdb import create_tables, get_session
from backend.app.cruds.add_crud import add_genre_start
from backend.app.validating_data import genres_list

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    async for session in get_session():
        for genre in genres_list:
            try:
                await add_genre_start(session=session, data=genre)
            except:
                pass
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_routes)
app.include_router(add_routes)
app.include_router(changes_routes)
app.include_router(getter_routes)
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from api.v1.add_routes import router as add_routes
from api.v1.changes_routes import router as changes_routes
from api.v1.getter_routes import router as getter_routes
from api.v1.users_routes import router as users_routes
from databases.postgresdb import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI()

app.include_router(users_routes)
app.include_router(add_routes)
app.include_router(changes_routes)
app.include_router(getter_routes)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
from fastapi import FastAPI
import uvicorn

from api.v1.chages_routes import router as changes_routes
from api.v1.comments_routes import router as comments_routes
from api.v1.tickets_routes import router as ticket_routes
from api.v1.travel_routes import router as travel_routes


app = FastAPI()

app.include_router(changes_routes)
app.include_router(comments_routes)
app.include_router(ticket_routes)
app.include_router(travel_routes)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
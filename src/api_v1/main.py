"""The main FastAPI application."""

import logging
from fastapi import FastAPI

import uvicorn


from server.database import init_db
from routes.house import router as HouseRouter


logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(HouseRouter, tags=["Houses"], prefix="/houses")


# deprecated! learn and switch to lifespan events in the future
@app.on_event("startup")
async def start_db():
    """Initialize the database connection on startup."""
    await init_db()


@app.get("/")
def root():
    """Welcome message for the API"""
    return {"message": "Welcome to the bnb homes API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

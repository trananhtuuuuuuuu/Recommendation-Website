from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import engine
from app.db.utils import check_db_connection

async def startup_event(app: FastAPI):
    """Mission: Handle all logic required when the app starts."""
    print("Starting up...")
    check_db_connection(engine)
    # You can add other startup missions here later (e.g., connecting to Redis)

async def shutdown_event(app: FastAPI):
    """Mission: Handle all logic required when the app stops."""
    print("Shutting down: Cleaning up resources...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event(app)
    yield
    await shutdown_event(app)
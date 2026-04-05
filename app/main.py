from fastapi import FastAPI
from app.lifespan import lifespan
from app.routes.api import api_router

def create_application() -> FastAPI:
    """Factory function to initialize the FastAPI app."""
    application = FastAPI(
        title="Recommenddation Weisite init",
        version="1.0.0",
        lifespan=lifespan
    )

    # Include your routes
    application.include_router(api_router, prefix="/api/v1")

    return application

app = create_application()
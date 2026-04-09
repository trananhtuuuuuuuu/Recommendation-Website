from fastapi import FastAPI
from app.api.v1.applicants.base import router as applicants_router

app = FastAPI(title="Recommendation Website Apis service")

# Include applicants router (contains /register endpoint)
app.include_router(applicants_router)
# app/main.py
from fastapi import FastAPI
from app.api.v1.applicants.applicant_endpoint import applicant_endpoint

app = FastAPI(title="Recommendation Website Apis service")


app.include_router(applicant_endpoint.router, prefix="/applicants",tags=["Applicants"])
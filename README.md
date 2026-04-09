# Overview
Name Project: Recommendation Website
Purpose: This is the final project for graduating at the University of Science in HCM City - Computer Science Major
Timeline: From Feb to July 2026

# Introduction
- This is a website is created for using recruiter and applicant
- To recruiters:
  - Recruiters can post Job that need anyone which is currently want to expose and excite can apply on that
- To Applicants:
  - Applicants can view all jobs shown on that with active status and also know how many percentage this job fit with them due to the AI Suggestion of this website

# Technical
- Backend: Python, Fastapi
- Database: PostgreSQL, Index, Concurrency controll, SQLAlchemy (ORM), Pydantic (validation data)
- Frontend: React, TypeScript, HTML, CSS, Tailwind
- Devops: CI, CD, AWS, Docker
- AI: Langchain

# Technique
- Backend:
- Database:
- Frontend:
- Devops:


# POST
 - /api/v1/users/auth (applicant or recruiter login)
 - /api/v1/applicants/registrations (applicant's registration)
 - /api/v1/recruiters/registrations (recruiter's registration)
 - /api/v1/applicants/upload-cv (a applicant upload cv)
 - /api/v1/recruiters/jobs (recruiter post a job)
# GET
 - / (view dashboard)
 - /api/v1/users/id (view user's profile)
 - /api/v1/users/notifications/id (view notification for user)
 - /api/v1/recruiters (get all recruiters currently Active in system)
 - /api/v1/jobs/{jobb_id}/applicants (View all applicants who applied for the certain job)
 - /api/v1/recruiters/{recruiter_id}/jobs (view all jobs that posted by the certain recruiter)
 - /api/v1/jobs (view all jobs)
# PUT

# DELETE

# PATCH
 - /api/v1/users/id (update the user's detail information)

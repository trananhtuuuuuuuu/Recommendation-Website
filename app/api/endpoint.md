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
# PUT

# DELETE

# PATCH
 - /api/v1/users/id (update the user's detail information)


 - Browse jobs (/api/v1/jobs)
  + des:
    - Role name:
    - company name:
    - job type:
    - working location:
    - working type
    - posting date:
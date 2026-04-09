from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.models.applicant import Applicant
from app.models.applicant_jd import ApplicantJD
from app.models.cv import Cv
from app.models.enums import ApplicantStatus, GenderEnum, MethodEnum
from app.models.job_description import JobDescription
from app.models.permission import Permission
from app.models.recruiter import Recruiter
from app.models.role import Role
from app.models.user import User


def get_or_create_role(db, role_name: str, description: str) -> Role:
    role = db.query(Role).filter(Role.role_name == role_name).first()
    if role:
        return role

    role = Role(role_name=role_name, description=description)
    db.add(role)
    db.flush()
    return role


def get_or_create_permission(db, endpoint: str, method: MethodEnum, description: str) -> Permission:
    permission = (
        db.query(Permission)
        .filter(Permission.endpoint == endpoint)
        .filter(Permission.method == method)
        .first()
    )
    if permission:
        return permission

    permission = Permission(endpoint=endpoint, method=method, description=description)
    db.add(permission)
    db.flush()
    return permission


def get_or_create_user(
    db,
    *,
    email: str,
    user_name: str,
    role: Role,
    address: str,
    phone_number: str,
    password: str,
) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Backward compatibility: update old plain-text seeded passwords.
        expected_hash = hash_password(password)
        if user.password != expected_hash:
            user.password = expected_hash
            db.flush()
        return user

    user = User(
        email=email,
        user_name=user_name,
        role_id=role.id,
        address=address,
        phone_number=phone_number,
        password=hash_password(password),
        access_token="",
        refresh_token="",
    )
    db.add(user)
    db.flush()
    return user


def seed() -> None:
    db = SessionLocal()
    try:
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

        admin_role = get_or_create_role(db, "ADMIN", "System administrator")
        recruiter_role = get_or_create_role(db, "RECRUITER", "Recruiter role")
        applicant_role = get_or_create_role(db, "APPLICANT", "Applicant role")

        jobs_permission = get_or_create_permission(
            db,
            endpoint="/api/v1/jobs",
            method=MethodEnum.GET,
            description="Read active jobs",
        )

        if jobs_permission not in recruiter_role.permissions:
            recruiter_role.permissions.append(jobs_permission)
        if jobs_permission not in applicant_role.permissions:
            applicant_role.permissions.append(jobs_permission)
        if jobs_permission not in admin_role.permissions:
            admin_role.permissions.append(jobs_permission)

        recruiter_user = get_or_create_user(
            db,
            email="recruiter.seed@datn.local",
            user_name="recruiter_seed",
            role=recruiter_role,
            address="Hanoi",
            phone_number="+84901234567",
            password="SeedPassword123",
        )

        recruiter = db.query(Recruiter).filter(Recruiter.id == recruiter_user.id).first()
        if recruiter is None:
            recruiter = Recruiter(
                id=recruiter_user.id,
                company_name="DATN Technologies",
                opening_date=date.today() - timedelta(days=365),
            )
            db.add(recruiter)
            db.flush()

        applicant_user = get_or_create_user(
            db,
            email="applicant.seed@datn.local",
            user_name="applicant_seed",
            role=applicant_role,
            address="Ho Chi Minh City",
            phone_number="+84908765432",
            password="SeedPassword123",
        )

        cv = db.query(Cv).filter(Cv.phone_number == applicant_user.phone_number).first()
        if cv is None:
            cv = Cv(
                full_name="Seed Applicant",
                address=applicant_user.address,
                phone_number=applicant_user.phone_number,
                objective="Become a backend engineer",
                skill="Python, FastAPI, PostgreSQL",
                gpa=3.4,
                experience="1 year internship",
                education="BSc Computer Science",
                certificate="TOEIC 800",
            )
            db.add(cv)
            db.flush()

        applicant = db.query(Applicant).filter(Applicant.id == applicant_user.id).first()
        if applicant is None:
            applicant = Applicant(
                id=applicant_user.id,
                applicant_status=ApplicantStatus.OpenToWork,
                gender=GenderEnum.male,
                full_name="Seed Applicant",
                data_of_birth=date(2000, 1, 1),
                cv_id=cv.id,
            )
            db.add(applicant)
            db.flush()

        active_job = db.query(JobDescription).filter(JobDescription.job_name == "Backend Engineer").first()
        if active_job is None:
            active_job = JobDescription(
                job_name="Backend Engineer",
                about_job="Build APIs for recommendation platform",
                responsibilities="Design services, write tests, support deployments",
                requirements="Python, SQLAlchemy, PostgreSQL",
                benefit="Hybrid work, health insurance",
                start_date=now_utc - timedelta(days=1),
                end_date=now_utc + timedelta(days=45),
                recruiter_id=recruiter.id,
            )
            db.add(active_job)
            db.flush()

        archived_job = db.query(JobDescription).filter(JobDescription.job_name == "Data Analyst Intern").first()
        if archived_job is None:
            archived_job = JobDescription(
                job_name="Data Analyst Intern",
                about_job="Support dashboard and reporting",
                responsibilities="Prepare reports and clean datasets",
                requirements="SQL basics, Excel",
                benefit="Mentorship",
                start_date=now_utc - timedelta(days=90),
                end_date=now_utc - timedelta(days=15),
                recruiter_id=recruiter.id,
            )
            db.add(archived_job)
            db.flush()

        has_application = (
            db.query(ApplicantJD)
            .filter(ApplicantJD.applicant_id == applicant.id)
            .filter(ApplicantJD.jd_id == active_job.id)
            .first()
        )
        if has_application is None:
            db.add(ApplicantJD(applicant_id=applicant.id, jd_id=active_job.id))

        db.commit()
        print("Seed data inserted/updated successfully.")
    except Exception as exc:
        db.rollback()
        raise RuntimeError(f"Failed to seed database: {exc}") from exc
    finally:
        db.close()


if __name__ == "__main__":
    seed()

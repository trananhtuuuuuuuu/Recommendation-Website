from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.job_description import JobDescription


def test_get_active_jobs_returns_only_active_rows():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = testing_session_local()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    db.add_all(
        [
            JobDescription(
                job_name="Active Job",
                about_job="desc",
                start_date=now - timedelta(days=1),
                end_date=now + timedelta(days=1),
            ),
            JobDescription(
                job_name="Expired Job",
                about_job="desc",
                start_date=now - timedelta(days=3),
                end_date=now - timedelta(days=1),
            ),
            JobDescription(
                job_name="Upcoming Job",
                about_job="desc",
                start_date=now + timedelta(days=1),
                end_date=now + timedelta(days=3),
            ),
            JobDescription(
                job_name="No End Date Active",
                about_job="desc",
                start_date=now - timedelta(days=1),
                end_date=None,
            ),
        ]
    )
    db.commit()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    response = client.get("/api/v1/jobs")

    assert response.status_code == 200
    body = response.json()
    names = {item["job_name"] for item in body}

    assert names == {"Active Job", "No End Date Active"}

    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=engine)

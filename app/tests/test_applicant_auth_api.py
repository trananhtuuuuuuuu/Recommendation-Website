from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


def _build_test_client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = testing_session_local()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client, db, engine


def _cleanup(db, engine):
    app.dependency_overrides.clear()
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_applicant_login_and_refresh_flow():
    client, db, engine = _build_test_client()
    try:
        register_payload = {
            "full_name": "Auth Applicant",
            "gender": "male",
            "phone_number": "+84901111222",
            "email": "auth.applicant@example.com",
            "user_name": "auth_applicant",
            "password": "AuthPass123",
            "address": "Hanoi",
            "date_of_birth": "2000-01-01",
            "applicant_status": "OpenToWork",
        }

        register_response = client.post("/applicants/register", json=register_payload)
        assert register_response.status_code == 201

        login_response = client.post(
            "/applicants/login",
            json={"identifier": "auth.applicant@example.com", "password": "AuthPass123"},
        )
        assert login_response.status_code == 200

        login_body = login_response.json()
        assert "access_token" in login_body
        assert "refresh_token" in login_body
        assert login_body["token_type"] == "bearer"

        refresh_response = client.post(
            "/applicants/refresh-token",
            json={"refresh_token": login_body["refresh_token"]},
        )
        assert refresh_response.status_code == 200

        refresh_body = refresh_response.json()
        assert "access_token" in refresh_body
        assert "refresh_token" in refresh_body
        assert refresh_body["token_type"] == "bearer"
    finally:
        _cleanup(db, engine)


def test_applicant_login_invalid_password_returns_401():
    client, db, engine = _build_test_client()
    try:
        register_payload = {
            "full_name": "Auth Applicant",
            "gender": "male",
            "phone_number": "+84902222333",
            "email": "invalid.pass@example.com",
            "user_name": "invalid_pass_user",
            "password": "AuthPass123",
            "address": "Hanoi",
            "date_of_birth": "2000-01-01",
            "applicant_status": "OpenToWork",
        }

        register_response = client.post("/applicants/register", json=register_payload)
        assert register_response.status_code == 201

        login_response = client.post(
            "/applicants/login",
            json={"identifier": "invalid.pass@example.com", "password": "WrongPass123"},
        )

        assert login_response.status_code == 401
    finally:
        _cleanup(db, engine)

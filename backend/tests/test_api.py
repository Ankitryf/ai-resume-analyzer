from datetime import datetime

from app.models import AnalysisResult, JobDescription, Resume, User


def register_and_login(client, username="testuser", email="test@example.com"):
    password = "testpassword123"
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_register_user(client):
    token = register_and_login(client)
    assert token


def test_missing_required_fields(client):
    response = client.post("/api/auth/register", json={})
    assert response.status_code == 422


def test_user_me_requires_authentication(client):
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_user_cannot_read_another_user(client):
    token = register_and_login(client)
    register_and_login(client, username="other", email="other@example.com")

    response = client.get("/api/users/2", headers=auth_headers(token))

    assert response.status_code == 403


def test_user_can_export_own_data(client, db):
    token = register_and_login(client)
    user = db.query(User).filter(User.username == "testuser").first()
    resume = Resume(
        user_id=user.id,
        filename="resume.pdf",
        file_path="uploads/resume.pdf",
        original_text="Resume text",
    )
    job = JobDescription(title="Job", content="Job description")
    db.add_all([resume, job])
    db.flush()
    db.add(
        AnalysisResult(
            user_id=user.id,
            resume_id=resume.id,
            job_description_id=job.id,
            ats_score=80,
            format_score=90,
            relevance_score=70,
            summary="Summary",
            hiring_recommendation="Strong Match",
            readiness_level="Ready Now",
            created_at=datetime.utcnow(),
        )
    )
    db.commit()

    response = client.get("/api/users/me/export", headers=auth_headers(token))

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["username"] == "testuser"
    assert body["analyses"][0]["resume"]["originalText"] == "Resume text"


def test_delete_account_deactivates_user(client):
    token = register_and_login(client)

    response = client.delete("/api/users/me", headers=auth_headers(token))
    assert response.status_code == 204

    response = client.get("/api/users/me", headers=auth_headers(token))
    assert response.status_code == 401


def test_analyze_requires_ai_consent(client):
    token = register_and_login(client)

    response = client.post(
        "/api/analyze",
        headers=auth_headers(token),
        data={"jobDescription": "Python developer", "aiProcessingConsent": "false"},
        files={"resume": ("resume.pdf", b"%PDF-1.4\n", "application/pdf")},
    )

    assert response.status_code == 400
    assert "consent" in response.json()["detail"].lower()


def test_analyze_rejects_invalid_pdf_magic_bytes(client):
    token = register_and_login(client)

    response = client.post(
        "/api/analyze",
        headers=auth_headers(token),
        data={"jobDescription": "Python developer", "aiProcessingConsent": "true"},
        files={"resume": ("resume.pdf", b"not a pdf", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid PDF file."


def test_deleted_analysis_is_not_returned(client, db):
    token = register_and_login(client)
    user = db.query(User).filter(User.username == "testuser").first()
    resume = Resume(
        user_id=user.id,
        filename="resume.pdf",
        file_path="uploads/resume.pdf",
        original_text="Resume text",
    )
    db.add(resume)
    db.flush()
    analysis = AnalysisResult(
        user_id=user.id,
        resume_id=resume.id,
        ats_score=80,
        format_score=90,
        relevance_score=70,
        summary="Summary",
        hiring_recommendation="Strong Match",
        readiness_level="Ready Now",
        deleted_at=datetime.utcnow(),
    )
    db.add(analysis)
    db.commit()

    response = client.get(f"/api/analysis/{analysis.id}", headers=auth_headers(token))

    assert response.status_code == 404

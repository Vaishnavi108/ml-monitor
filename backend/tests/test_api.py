import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health_check():
    r = client.get("/api/v1/metrics/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_prediction():
    payload = {
        "age": 35,
        "education_num": 13,
        "hours_per_week": 40,
        "capital_gain": 0,
        "capital_diff": 0
    }
    r = client.post("/api/v1/predictions/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["prediction"] in [0, 1]
    assert 0.0 <= data["confidence"] <= 1.0

def test_list_predictions():
    r = client.get("/api/v1/predictions/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_stats():
    r = client.get("/api/v1/predictions/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_predictions" in data
    assert "avg_confidence" in data
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
from app import models, schemas, crud

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_create_item():
    response = client.post(
        "/items/",
        json={"title": "Test Item", "description": "This is a test item", "owner_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Item"

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Item"

def test_update_item():
    response = client.put(
        "/items/1",
        json={"title": "Updated Test Item", "description": "This is an updated test item"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Item"

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Item"

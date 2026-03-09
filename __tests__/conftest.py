import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from app.dependencies.database import get_db
from app.models.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 👇 scope="function" garantiza DB limpia por cada test
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_client(client):
    """Registra un usuario de prueba y retorna (client, headers, user_id)"""
    reg = client.post("/login/create", json={
        "name": "Test User",
        "mail": "testuser@test.com",
        "pass_": "123456"
    })
    assert reg.status_code == 200, f"Fallo al registrar usuario: {reg.json()}"

    response = client.post("/login", json={
        "mail": "testuser@test.com",
        "pass_": "123456"
    })
    assert response.status_code == 200, f"Fallo en login: {response.json()}"

    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    from jose import jwt
    import os
    payload = jwt.decode(
        token,
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")]
    )
    user_id = payload["user_id"]

    return client, headers, user_id
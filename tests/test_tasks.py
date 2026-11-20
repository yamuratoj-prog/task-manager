import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    # Отдельная БД в памяти для каждого теста
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get_task(client):
    r = client.post("/tasks", json={"title": "Купить молоко", "description": "2 литра"})
    assert r.status_code == 201
    task = r.json()
    assert task["title"] == "Купить молоко"
    assert task["done"] is False

    r = client.get(f"/tasks/{task['id']}")
    assert r.status_code == 200
    assert r.json()["description"] == "2 литра"


def test_validation_error(client):
    r = client.post("/tasks", json={"title": ""})
    assert r.status_code == 422


def test_list_and_filter(client):
    client.post("/tasks", json={"title": "A"})
    t2 = client.post("/tasks", json={"title": "B"}).json()
    client.patch(f"/tasks/{t2['id']}", json={"done": True})

    assert len(client.get("/tasks").json()) == 2
    done = client.get("/tasks", params={"done": True}).json()
    assert [t["title"] for t in done] == ["B"]


def test_update_task(client):
    t = client.post("/tasks", json={"title": "Старое"}).json()
    r = client.patch(f"/tasks/{t['id']}", json={"title": "Новое", "done": True})
    assert r.status_code == 200
    assert r.json()["title"] == "Новое"
    assert r.json()["done"] is True


def test_delete_task(client):
    t = client.post("/tasks", json={"title": "Удалить меня"}).json()
    assert client.delete(f"/tasks/{t['id']}").status_code == 204
    assert client.get(f"/tasks/{t['id']}").status_code == 404


def test_not_found(client):
    assert client.get("/tasks/999").status_code == 404
    assert client.patch("/tasks/999", json={"done": True}).status_code == 404
    assert client.delete("/tasks/999").status_code == 404

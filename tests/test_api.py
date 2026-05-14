import pytest
from fastapi.testclient import TestClient
from main import app
from models.storage import books_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    books_db.clear()
    yield

def test_create_book():
    response = client.post("/books/", json={
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "description": "Збірка",
        "status": "available",
        "year": 1840
    })
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_books():
    client.post("/books/", json={"title": "Книга", "author": "Автор", "year": 2020, "status": "available"})
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_book_by_id():
    post_res = client.post("/books/", json={"title": "Книга", "author": "Автор", "year": 2021, "status": "available"})
    book_id = post_res.json()["id"]
    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 200

def test_get_book_not_found():
    response = client.get("/books/fake-id")
    assert response.status_code == 404

def test_delete_book():
    post_res = client.post("/books/", json={"title": "Книга", "author": "Автор", "year": 2022, "status": "available"})
    book_id = post_res.json()["id"]
    assert client.delete(f"/books/{book_id}").status_code == 204
    assert client.delete(f"/books/{book_id}").status_code == 204
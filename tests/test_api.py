import pytest
from fastapi.testclient import TestClient
from main import app
from models.storage import books_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    
    books_db.clear()

def test_create_book():
    response = client.post("/books/", json={
        "title": "Кобзар",
        "author": "Тарас Шевченко",
        "year": 1840,
        "status": "наявні в бібліотеці"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Кобзар"
    assert "id" in data

def test_get_all_books():
    client.post("/books/", json={"title": "1984", "author": "Джордж Орвелл", "year": 1949, "status": "наявні в бібліотеці"})
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_book_by_id():
  
    create_res = client.post("/books/", json={"title": "Маруся", "author": "Г. Квітка-Основ'яненко", "year": 1834})
    book_id = create_res.json()["id"]
    
   
    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == book_id

def test_delete_book_idempotent():
    import uuid
    random_id = str(uuid.uuid4())
    
   
    response1 = client.delete(f"/books/{random_id}")
    assert response1.status_code == 204
    

    response2 = client.delete(f"/books/{random_id}")
    assert response2.status_code == 204
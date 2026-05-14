import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from models.storage import books_db

@pytest.fixture(autouse=True)
def clear_db():
    books_db.clear()

@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books", json={
            "title": "A",
            "author": "B",
            "description": "C",
            "status": "available",
            "year": 2026
        })
    assert response.status_code == 201
    assert response.json()["title"] == "A"
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/books", json={
            "title": "A", 
            "author": "B", 
            "description": "C", 
            "status": "available", 
            "year": 2026
        })
        response = await ac.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_get_book_by_id():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_resp = await ac.post("/books", json={
            "title": "A", 
            "author": "B", 
            "description": "C", 
            "status": "available", 
            "year": 2026
        })
        book_id = create_resp.json()["id"]
        response = await ac.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id

@pytest.mark.asyncio
async def test_delete_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_resp = await ac.post("/books", json={
            "title": "A", 
            "author": "B", 
            "description": "C", 
            "status": "available", 
            "year": 2026
        })
        book_id = create_resp.json()["id"]
        
        del_resp = await ac.delete(f"/books/{book_id}")
        assert del_resp.status_code == 204
        
        get_resp = await ac.get(f"/books/{book_id}")
        assert get_resp.status_code == 404
        
        del_resp_again = await ac.delete(f"/books/{book_id}")
        assert del_resp_again.status_code == 204
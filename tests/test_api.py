import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books/", json={
            "title": "SQLAlchemy Guide",
            "author": "Tech Author",
            "description": "Learning ORM",
            "status": "наявна в бібліотеці",
            "release_year": 2023
        })
    assert response.status_code == 201
    assert response.json()["title"] == "SQLAlchemy Guide"

@pytest.mark.asyncio
async def test_pagination():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for i in range(5):
            await ac.post("/books/", json={
                "title": f"Book {i}",
                "author": "Author",
                "status": "наявна в бібліотеці",
                "release_year": 2020 + i
            })
        
        response = await ac.get("/books/?limit=2&offset=0")
        assert response.status_code == 200
        assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_delete_idempotency():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        post_res = await ac.post("/books/", json={
            "title": "Temp",
            "author": "Author",
            "status": "наявна в бібліотеці",
            "release_year": 2022
        })
        book_id = post_res.json()["id"]
        
        res1 = await ac.delete(f"/books/{book_id}")
        assert res1.status_code == 204
        
        res2 = await ac.delete(f"/books/{book_id}")
        assert res2.status_code == 204
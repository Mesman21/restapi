import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_and_paginate_books(client: AsyncClient):
    
    books_to_create = [
        {"title": "Test Book 1", "author": "Author 1", "status": "наявна в бібліотеці", "release_year": 2024},
        {"title": "Test Book 2", "author": "Author 2", "status": "наявна в бібліотеці", "release_year": 2024},
        {"title": "Test Book 3", "author": "Author 3", "status": "наявна в бібліотеці", "release_year": 2024},
    ]
    
    for book in books_to_create:
        await client.post("/books/", json=book)

    
    response = await client.get("/books/?limit=2&offset=0")
    assert response.status_code == 200
    data_page_1 = response.json()
    assert isinstance(data_page_1, list)
    assert len(data_page_1) == 2

   
    response = await client.get("/books/?limit=2&offset=2")
    assert response.status_code == 200
    data_page_2 = response.json()
    
    
    assert len(data_page_2) >= 1
    assert data_page_2[0]["id"] != data_page_1[0]["id"]

@pytest.mark.asyncio
async def test_get_book_by_id(client: AsyncClient):
    book_data = {"title": "Unique Book", "author": "Author", "status": "наявна в бібліотеці", "release_year": 2024}
    create_res = await client.post("/books/", json=book_data)
    book_id = create_res.json()["id"]

    response = await client.get(f"/books/{book_id}") 
    assert response.status_code == 200
    assert response.json()["title"] == "Unique Book"
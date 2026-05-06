import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_cursor_pagination():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for i in range(5):
            await ac.post("/books/", json={
                "title": f"Cursor Book {i}",
                "author": "Author",
                "status": "наявна в бібліотеці",
                "release_year": 2020
            })
        
        res1 = await ac.get("/books/?limit=2")
        data1 = res1.json()
        assert len(data1["items"]) == 2
        assert data1["next_cursor"] is not None
        
        next_cursor = data1["next_cursor"]
        res2 = await ac.get(f"/books/?limit=2&cursor={next_cursor}")
        data2 = res2.json()
        assert len(data2["items"]) <= 2
        assert data2["items"][0]["id"] != data1["items"][0]["id"]
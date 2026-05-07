import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from database import get_users_col, get_books_col

@pytest.mark.asyncio
async def test_auth_and_books():
    # 1. Створюємо транспорт для FastAPI
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        # КРОК 0: ГАРАНТОВАНЕ ОЧИЩЕННЯ
        # Видаляємо дані прямо тут, щоб уникнути помилки 400
        await get_users_col().delete_many({})
        await get_books_col().delete_many({})

        # 1. Реєстрація (тепер точно 200, бо ми щойно все видалили)
        user_data = {"username": "testuser", "password": "password123"}
        reg_resp = await ac.post("/auth/register", json=user_data)
        assert reg_resp.status_code == 200

        # 2. Логін
        login_resp = await ac.post("/auth/login", data=user_data)
        assert login_resp.status_code == 200
        tokens = login_resp.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        # 3. Перевірка доступу (Додаємо книгу)
        headers = {"Authorization": f"Bearer {access_token}"}
        book_data = {
            "title": "FastAPI Lab 6",
            "author": "Jaroslav",
            "status": "available",
            "year": 2026
        }
        post_resp = await ac.post("/books/", json=book_data, headers=headers)
        assert post_resp.status_code == 201

        # 4. Перевірка Refresh Token
        refresh_resp = await ac.post(f"/auth/refresh?refresh_token={refresh_token}")
        assert refresh_resp.status_code == 200
        assert "access_token" in refresh_resp.json()
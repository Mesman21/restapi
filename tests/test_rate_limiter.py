import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from main import app


def mock_redis_pipeline(mock_get_redis, zcard_return_value):
   
    mock_pipe = MagicMock() 
  
    mock_pipe.execute = AsyncMock(return_value=[1, zcard_return_value, 1, True]) 
    
    mock_pipeline_manager = MagicMock()
    mock_pipeline_manager.__aenter__ = AsyncMock(return_value=mock_pipe)
    mock_pipeline_manager.__aexit__ = AsyncMock(return_value=None)
    
    mock_redis_instance = MagicMock()
    mock_redis_instance.pipeline.return_value = mock_pipeline_manager
    
    mock_get_redis.return_value = mock_redis_instance


@pytest.mark.asyncio
@patch("api.endpoints.BookService.get_books", new_callable=AsyncMock) 
@patch("middlewares.rate_limiter.get_redis")
async def test_anonymous_under_limit(mock_get_redis, mock_get_books):
    mock_get_books.return_value = [] 
    mock_redis_pipeline(mock_get_redis, zcard_return_value=1)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/books/")
        assert res.status_code == 200

@pytest.mark.asyncio
@patch("api.endpoints.BookService.get_books", new_callable=AsyncMock)
@patch("middlewares.rate_limiter.get_redis")
async def test_anonymous_over_limit(mock_get_redis, mock_get_books):
    mock_get_books.return_value = []
    mock_redis_pipeline(mock_get_redis, zcard_return_value=2)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/books/")
        assert res.status_code == 429

@pytest.mark.asyncio
@patch("api.endpoints.BookService.get_books", new_callable=AsyncMock)
@patch("middlewares.rate_limiter.get_current_user")
@patch("middlewares.rate_limiter.get_redis")
async def test_authenticated_under_limit(mock_get_redis, mock_get_user, mock_get_books):
    mock_get_books.return_value = []
    mock_get_user.return_value = {"username": "testuser"}
    mock_redis_pipeline(mock_get_redis, zcard_return_value=9)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/books/", headers={"Authorization": "Bearer token"})
        assert res.status_code == 200

@pytest.mark.asyncio
@patch("api.endpoints.BookService.get_books", new_callable=AsyncMock)
@patch("middlewares.rate_limiter.get_current_user")
@patch("middlewares.rate_limiter.get_redis")
async def test_authenticated_over_limit(mock_get_redis, mock_get_user, mock_get_books):
    mock_get_books.return_value = []
    mock_get_user.return_value = {"username": "testuser"}
    mock_redis_pipeline(mock_get_redis, zcard_return_value=10)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/books/", headers={"Authorization": "Bearer token"})
        assert res.status_code == 429
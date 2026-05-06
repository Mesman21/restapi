from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from repository.book_repository import BookRepository
from schemas.book import BookCreate, BookStatus

class BookService:
    def __init__(self, session: AsyncSession):
        self.repository = BookRepository(session)

    async def get_books(self, limit: int, offset: int, status: Optional[BookStatus], author: Optional[str], sort_by: Optional[str]):
        return await self.repository.get_all(limit, offset, status, author, sort_by)

    async def get_book(self, book_id: UUID):
        return await self.repository.get_by_id(book_id)

    async def create_book(self, book_in: BookCreate):
        return await self.repository.create(book_in)

    async def delete_book(self, book_id: UUID):
        await self.repository.delete(book_id)
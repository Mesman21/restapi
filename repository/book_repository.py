from sqlalchemy import select, delete, update, asc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from uuid import UUID
from models.books import BookModel
from schemas.book import BookCreate, BookStatus

class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_cursor(
        self, 
        limit: int, 
        cursor: Optional[UUID] = None, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None
    ) -> Tuple[List[BookModel], Optional[UUID]]:
        query = select(BookModel).order_by(asc(BookModel.id)).limit(limit + 1)
        
        if cursor:
            query = query.where(BookModel.id > cursor)
        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author.ilike(f"%{author}%"))
            
        result = await self.session.execute(query)
        items = list(result.scalars().all())
        
        next_cursor = None
        if len(items) > limit:
            next_cursor = items[limit - 1].id
            items = items[:limit]
            
        return items, next_cursor

    async def get_by_id(self, book_id: UUID) -> Optional[BookModel]:
        query = select(BookModel).where(BookModel.id == book_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, book_data: BookCreate) -> BookModel:
        new_book = BookModel(**book_data.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def delete(self, book_id: UUID) -> None:
        query = delete(BookModel).where(BookModel.id == book_id)
        await self.session.execute(query)
        await self.session.commit()
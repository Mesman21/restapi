from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from models.books import BookModel
from schemas.book import BookCreate, BookStatus

class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self, 
        limit: int, 
        offset: int, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> List[BookModel]:
        query = select(BookModel).offset(offset).limit(limit)
        
        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author.ilike(f"%{author}%"))
            
        if sort_by == "title":
            query = query.order_by(BookModel.title)
        elif sort_by == "release_year":
            query = query.order_by(BookModel.release_year)
            
        result = await self.session.execute(query)
        return result.scalars().all()

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
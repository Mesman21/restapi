from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from database import get_db
from schemas.book import Book, BookCreate, BookStatus, BookCursorPaginationResponse
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=BookCursorPaginationResponse, status_code=status.HTTP_200_OK)
async def get_all_books(
    limit: int = Query(10, ge=1, le=100),
    cursor: Optional[UUID] = None,
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    service = BookService(db)
    items, next_cursor = await service.repository.get_all_cursor(limit, cursor, status, author)
    return {"items": items, "next_cursor": next_cursor}

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    book = await service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.create_book(book_in)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    await service.delete_book(book_id)
    return None
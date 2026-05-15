from fastapi import APIRouter, HTTPException, status, Query, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from uuid import UUID
from database import get_db
from schemas.book import Book, BookCreate
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    service = BookService(db)
    return await service.repository.get_all(limit, offset)

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = BookService(db)
    book = await service.repository.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_in: BookCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = BookService(db)
    return await service.repository.create(book_in)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncIOMotorDatabase = Depends(get_db)):
    service = BookService(db)
    success = await service.repository.delete(book_id)
    if not success:
        pass
    return None
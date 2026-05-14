from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService

router = APIRouter()
book_service = BookService()

@router.get("/books", response_model=List[BookResponse])
async def get_books(
    author: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None)
):
    return await book_service.get_all_books(author=author, status=status, sort_by=sort_by)

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: uuid.UUID):
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await book_service.create_book(book)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: uuid.UUID):
    await book_service.delete_book(book_id)
    return None
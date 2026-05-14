from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from schemas.book import BookCreate, BookResponse, BookStatus, SortBy
from services.book_service import BookService

router = APIRouter()
book_service = BookService()

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    author: Optional[str] = Query(None),
    book_status: Optional[BookStatus] = Query(None, alias="status"),
    sort_by: Optional[SortBy] = Query(None)
):
    status_val = book_status.value if book_status else None
    sort_val = sort_by.value if sort_by else None
    return await book_service.get_all_books(author=author, status=status_val, sort_by=sort_val)

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: str):
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await book_service.create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    await book_service.delete_book(book_id)
    return
from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from uuid import UUID
from schemas.book import BookCreate, BookResponse, BookStatus
from services.book_service import BookService


router = APIRouter(tags=["Books"])

def get_service():
    return BookService()

@router.get("/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_all_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Сортування: 'title' або 'year'", pattern="^(title|year)$"),
    service: BookService = Depends(get_service)
):
    return await service.get_books(status, author, sort_by)

@router.get("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, service: BookService = Depends(get_service)):
    return await service.get_book_by_id(book_id)

@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, service: BookService = Depends(get_service)):
    return await service.create_book(book)

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, service: BookService = Depends(get_service)):
    await service.delete_book(book_id)
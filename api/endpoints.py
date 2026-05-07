from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from services.book_service import BookService
from services.auth_service import get_current_user
from schemas.book import BookResponse, BookCreate

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
async def get_books(
    status: Optional[str] = None, 
    author: Optional[str] = None, 
    sort_by: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    return await BookService.get_books(status, author, sort_by)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, current_user: dict = Depends(get_current_user)):
    return await BookService.create_book(book.model_dump())

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, current_user: dict = Depends(get_current_user)):
    book = await BookService.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, current_user: dict = Depends(get_current_user)):
    await BookService.delete_book(book_id)
    return None
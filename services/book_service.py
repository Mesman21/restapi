from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from schemas.book import BookCreate, BookResponse, BookStatus
from repository.book_repo import BookRepository

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(
        self, 
        status_filter: Optional[BookStatus] = None, 
        author_filter: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> List[Dict]:
        books = await self.repo.get_all()
        
       
        if status_filter:
            books = [b for b in books if b["status"] == status_filter.value]
        if author_filter:
            books = [b for b in books if b["author"].lower() == author_filter.lower()]
            
   
        if sort_by == "title":
            books.sort(key=lambda x: x["title"].lower())
        elif sort_by == "year":
            books.sort(key=lambda x: x["year"])
            
        return books

    async def get_book_by_id(self, book_id: UUID) -> Dict:
        book = await self.repo.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено")
        return book

    async def create_book(self, book_data: BookCreate) -> Dict:
        new_book = book_data.model_dump()
        new_book["id"] = uuid4()
        new_book["status"] = new_book["status"].value  
        return await self.repo.add(new_book)

    async def delete_book(self, book_id: UUID) -> None:
        
        await self.repo.delete(book_id)
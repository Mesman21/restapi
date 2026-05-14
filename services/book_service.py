import uuid
from typing import List, Dict, Optional
from repository.book_repo import BookRepository
from schemas.book import BookCreate

repo = BookRepository()

class BookService:
    async def get_all_books(
        self, author: Optional[str] = None, status: Optional[str] = None, sort_by: Optional[str] = None
    ) -> List[Dict]:
        books = await repo.get_all()
        
        if author:
            books = [b for b in books if b["author"].lower() == author.lower()]
        if status:
            books = [b for b in books if b["status"] == status]
            
        if sort_by == "title":
            books = sorted(books, key=lambda x: x["title"].lower())
        elif sort_by == "year":
            books = sorted(books, key=lambda x: x["year"])
            
        return books

    async def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        return await repo.get_by_id(book_id)

    async def create_book(self, book_in: BookCreate) -> Dict:
        book_dict = getattr(book_in, "model_dump", book_in.dict)()
        book_dict["id"] = str(uuid.uuid4())
        return await repo.create(book_dict)

    async def delete_book(self, book_id: str) -> None:
        await repo.delete(book_id)
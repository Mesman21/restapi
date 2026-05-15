from typing import List, Dict, Optional
from uuid import UUID
from models.storage import books_db

class BookRepository:
    async def get_all(self) -> List[Dict]:
        return books_db

    async def get_by_id(self, book_id: UUID) -> Optional[Dict]:
        for book in books_db:
            if book["id"] == book_id:
                return book
        return None

    async def add(self, book: Dict) -> Dict:
        books_db.append(book)
        return book

    async def delete(self, book_id: UUID) -> None:
        global books_db
        # Фільтруємо список, залишаючи всі книги, крім тої, що треба видалити
        books_db[:] = [book for book in books_db if book["id"] != book_id]
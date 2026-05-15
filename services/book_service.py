from motor.motor_asyncio import AsyncIOMotorDatabase
from repository.book_repository import BookRepository

class BookService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = BookRepository(db)
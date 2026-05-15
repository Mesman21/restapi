from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from uuid import UUID, uuid4
from schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.books

    async def get_all(self, limit: int, offset: int) -> List[dict]:
        cursor = self.collection.find().skip(offset).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_by_id(self, book_id: UUID) -> Optional[dict]:
        return await self.collection.find_one({"id": str(book_id)})

    async def create(self, book_data: BookCreate) -> dict:
        book_dict = book_data.model_dump()
        book_dict["id"] = str(uuid4())
        await self.collection.insert_one(book_dict)
        return book_dict

    async def delete(self, book_id: UUID) -> bool:
        result = await self.collection.delete_one({"id": str(book_id)})
        return result.deleted_count > 0
from bson import ObjectId
from database import get_books_col

class BookRepository:
    @staticmethod
    async def get_all(query, sort_by=None):
        books_collection = get_books_col() # Отримуємо тут
        cursor = books_collection.find(query)
        if sort_by in ['title', 'year']:
            cursor = cursor.sort(sort_by, 1)
        
        books = []
        async for book in cursor:
            book['_id'] = str(book['_id'])
            books.append(book)
        return books

    @staticmethod
    async def get_by_id(book_id):
        books_collection = get_books_col()
        book = await books_collection.find_one({"_id": ObjectId(book_id)})
        if book:
            book['_id'] = str(book['_id'])
        return book

    @staticmethod
    async def create(data):
        books_collection = get_books_col()
        result = await books_collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    @staticmethod
    async def delete(book_id):
        books_collection = get_books_col()
        await books_collection.delete_one({"_id": ObjectId(book_id)})